import json
import shutil
import subprocess
import textwrap

import pytest


def _run_plausible(consent_granted):
    script = textwrap.dedent(
        f"""
        var window={{}};
        var document={{body:{{dataset:{{analyticsProvider:'plausible',consentRequired:'true',consentGranted:'{str(consent_granted).lower()}'}}}}}};
        (function(){{
          var body=document.body;
          var p=body.dataset.analyticsProvider;
          function hasConsent(){{return body.dataset.consentRequired!=='true'||body.dataset.consentGranted==='true';}}
          function send(n,m){{if(!hasConsent())return;m=m||{{}};if(p==='plausible'&&window.plausible){{window.plausible(n,{{props:m}});}}
            else if(p==='ga4'&&window.gtag){{window.gtag('event',n,m);}}}}
          if (hasConsent()) {{ window.tfSend = send; }}
        }})();
        var calls=[];
        window.plausible=function(n,o){{calls.push([n,o]);}};
        if(window.tfSend) window.tfSend('evt',{{foo:'bar'}});
        console.log(JSON.stringify(calls));
        """
    )
    result = subprocess.run(['node', '-e', script], capture_output=True, text=True, check=True)
    return json.loads(result.stdout.strip())


def _run_ga4(consent_granted):
    script = textwrap.dedent(
        f"""
        var window={{}};
        var document={{body:{{dataset:{{analyticsProvider:'ga4',consentRequired:'true',consentGranted:'{str(consent_granted).lower()}'}}}}}};
        (function(){{
          var body=document.body;
          var p=body.dataset.analyticsProvider;
          function hasConsent(){{return body.dataset.consentRequired!=='true'||body.dataset.consentGranted==='true';}}
          function send(n,m){{if(!hasConsent())return;m=m||{{}};if(p==='plausible'&&window.plausible){{window.plausible(n,{{props:m}});}}
            else if(p==='ga4'&&window.gtag){{window.gtag('event',n,m);}}}}
          if (hasConsent()) {{ window.tfSend = send; }}
        }})();
        var calls=[];
        window.gtag=function(kind,name,meta){{calls.push([kind,name,meta]);}};
        if(window.tfSend) window.tfSend('evt',{{foo:'bar'}});
        console.log(JSON.stringify(calls));
        """
    )
    result = subprocess.run(['node', '-e', script], capture_output=True, text=True, check=True)
    return json.loads(result.stdout.strip())


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_tf_send_plausible_respects_consent():
    assert _run_plausible(False) == []


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_tf_send_plausible_sends_with_consent():
    assert _run_plausible(True) == [['evt', {'props': {'foo': 'bar'}}]]


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_tf_send_ga4_respects_consent():
    assert _run_ga4(False) == []


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_tf_send_ga4_sends_with_consent():
    assert _run_ga4(True) == [['event', 'evt', {'foo': 'bar'}]]

