import json
import shutil
import subprocess
import textwrap

import pytest


def _run_plausible(consent_granted, enabled=True, provide_api=True):
    script = textwrap.dedent(
        f"""
        var window={{}};
        var events={{}};
        var document={{body:{{dataset:{{analyticsProvider:'plausible',analyticsEnabled:'{str(enabled).lower()}',consentRequired:'true',consentGranted:'{str(consent_granted).lower()}'}}}},addEventListener:function(n,f){{events[n]=f;}}}};
        var logs=[];
        (function(){{
          var body=document.body;
          var p=body.dataset.analyticsProvider;
          var enabled=(body.dataset.analyticsEnabled||'true')==='true';
          function hasConsent(){{return body.dataset.consentRequired!=='true'||body.dataset.consentGranted==='true';}}
          function isActive(){{return enabled&&hasConsent();}}
          function log(k,d){{logs.push([k,d]);}}
          function send(n,m){{if(!isActive())return;m=m||{{}};try{{if(p==='plausible'&&window.plausible){{window.plausible(n,{{props:m}});log('info',{{event:n,meta:m,provider:p,ok:true}});}}else if(p==='ga4'&&window.gtag){{window.gtag('event',n,m);log('info',{{event:n,meta:m,provider:p,ok:true}});}}else{{log('warn',{{event:n,meta:m,provider:p,ok:false,reason:'provider-missing'}});}}}}catch(e){{log('error',{{event:n,meta:m,provider:p,ok:false,error:e.toString()}});}}}}
          if(isActive()){{window.tfSend=send;}}
          document.addEventListener('tf:consent-updated',function(){{if(isActive()&&!window.tfSend){{window.tfSend=send;}}}});
        }})();
        var calls=[];
        if({str(provide_api).lower()}) window.plausible=function(n,o){{calls.push([n,o]);}};
        if(window.tfSend) window.tfSend('evt',{{foo:'bar'}});
        console.log(JSON.stringify({{calls:calls,logs:logs}}));
        """
    )
    result = subprocess.run(['node', '-e', script], capture_output=True, text=True, check=True)
    return json.loads(result.stdout.strip())


def _run_ga4(consent_granted, enabled=True, provide_api=True):
    script = textwrap.dedent(
        f"""
        var window={{}};
        var events={{}};
        var document={{body:{{dataset:{{analyticsProvider:'ga4',analyticsEnabled:'{str(enabled).lower()}',consentRequired:'true',consentGranted:'{str(consent_granted).lower()}'}}}},addEventListener:function(n,f){{events[n]=f;}}}};
        var logs=[];
        (function(){{
          var body=document.body;
          var p=body.dataset.analyticsProvider;
          var enabled=(body.dataset.analyticsEnabled||'true')==='true';
          function hasConsent(){{return body.dataset.consentRequired!=='true'||body.dataset.consentGranted==='true';}}
          function isActive(){{return enabled&&hasConsent();}}
          function log(k,d){{logs.push([k,d]);}}
          function uid(){{try{{return crypto.randomUUID()}}catch(e){{return Date.now().toString(36)+Math.random().toString(36).slice(2);}}}}
          function send(n,m){{if(!isActive())return;m=m||{{}};var id=m.id||uid();m.id=id;try{{if(p==='plausible'&&window.plausible){{window.plausible(n,{{props:m}});log('info',{{id:id,event:n,meta:m,provider:p,ok:true}});}}else if(p==='ga4'&&window.gtag){{window.gtag('event',n,m);log('info',{{id:id,event:n,meta:m,provider:p,ok:true}});}}else{{log('warn',{{id:id,event:n,meta:m,provider:p,ok:false,reason:'provider-missing'}});}}}}catch(e){{log('error',{{id:id,event:n,meta:m,provider:p,ok:false,error:e.toString()}});}}}}
          if(isActive()){{window.tfSend=send;}}
          document.addEventListener('tf:consent-updated',function(){{if(isActive()&&!window.tfSend){{window.tfSend=send;}}}});
        }})();
        var calls=[];
        if({str(provide_api).lower()}) window.gtag=function(kind,name,meta){{calls.push([kind,name,meta]);}};
        if(window.tfSend) window.tfSend('evt',{{foo:'bar'}});
        console.log(JSON.stringify({{calls:calls,logs:logs}}));
        """
    )
    result = subprocess.run(['node', '-e', script], capture_output=True, text=True, check=True)
    return json.loads(result.stdout.strip())


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_tf_send_plausible_respects_consent():
    assert _run_plausible(False)["calls"] == []
    assert _run_plausible(False)["logs"] == []


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_tf_send_plausible_sends_with_consent():
    result = _run_plausible(True)
    call = result["calls"][0]
    assert call[0] == 'evt'
    assert call[1]['props']['foo'] == 'bar'
    assert 'id' in call[1]['props']
    log = result["logs"][0]
    assert log[0] == 'info'
    data = log[1]
    assert data['event'] == 'evt'
    assert data['provider'] == 'plausible'
    assert data['ok'] is True
    assert data['meta']['foo'] == 'bar'
    assert 'id' in data and data['id'] == data['meta']['id']


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_tf_send_logs_when_provider_missing():
    result = _run_plausible(True, provide_api=False)
    assert result["calls"] == []
    log = result["logs"][0]
    assert log[0] == 'warn'
    data = log[1]
    assert data['event'] == 'evt'
    assert data['provider'] == 'plausible'
    assert data['ok'] is False
    assert data['reason'] == 'provider-missing'
    assert 'id' in data and 'id' in data['meta']


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_tf_send_ga4_respects_consent():
    assert _run_ga4(False)["calls"] == []
    assert _run_ga4(False)["logs"] == []


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_tf_send_ga4_sends_with_consent():
    result = _run_ga4(True)
    call = result["calls"][0]
    assert call[0] == 'event'
    assert call[1] == 'evt'
    assert call[2]['foo'] == 'bar'
    assert 'id' in call[2]
    log = result["logs"][0]
    assert log[0] == 'info'
    data = log[1]
    assert data['event'] == 'evt'
    assert data['provider'] == 'ga4'
    assert data['ok'] is True
    assert data['meta']['foo'] == 'bar'
    assert 'id' in data and data['id'] == data['meta']['id']


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_tf_send_enables_after_consent_event():
    script = textwrap.dedent(
        """
        var window={};
        var events={};
        var document={body:{dataset:{analyticsProvider:'plausible',analyticsEnabled:'true',consentRequired:'true',consentGranted:'false'}},addEventListener:function(n,f){events[n]=f;}};
        var logs=[];
        (function(){
          var body=document.body;
          var p=body.dataset.analyticsProvider;
          var enabled=(body.dataset.analyticsEnabled||'true')==='true';
          function hasConsent(){return body.dataset.consentRequired!=='true'||body.dataset.consentGranted==='true';}
          function isActive(){return enabled&&hasConsent();}
          function log(k,d){logs.push([k,d]);}
          function uid(){try{return crypto.randomUUID()}catch(e){return Date.now().toString(36)+Math.random().toString(36).slice(2);}}
          function send(n,m){if(!isActive())return;m=m||{};var id=m.id||uid();m.id=id;try{if(p==='plausible'&&window.plausible){window.plausible(n,{props:m});log('info',{id:id,event:n,meta:m,provider:p,ok:true});}else if(p==='ga4'&&window.gtag){window.gtag('event',n,m);log('info',{id:id,event:n,meta:m,provider:p,ok:true});}else{log('warn',{id:id,event:n,meta:m,provider:p,ok:false,reason:'provider-missing'});}}catch(e){log('error',{id:id,event:n,meta:m,provider:p,ok:false,error:e.toString()});}}
          if(isActive()){window.tfSend=send;}
          document.addEventListener('tf:consent-updated',function(){if(isActive()&&!window.tfSend){window.tfSend=send;}});
        })();
        var calls=[];
        window.plausible=function(n,o){calls.push([n,o]);};
        if(window.tfSend) window.tfSend('pre',{});
        document.body.dataset.consentGranted='true';
        events['tf:consent-updated']();
        if(window.tfSend) window.tfSend('post',{});
        console.log(JSON.stringify({calls:calls,logs:logs}));
        """
    )
    result = subprocess.run(['node', '-e', script], capture_output=True, text=True, check=True)
    data = json.loads(result.stdout.strip())
    assert 'id' in data["calls"][0][1]['props']
    log = data["logs"][-1]
    assert log[0] == 'info'
    d = log[1]
    assert d['event'] == 'post'
    assert d['provider'] == 'plausible'
    assert d['ok'] is True
    assert 'id' in d and d['id'] == d['meta']['id']

