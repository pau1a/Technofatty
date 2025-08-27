# Tools: Product Line Charter

Tools are products. They must stand alone, teach by doing, and connect back into the rest of the site with intent.

## What qualifies as a tool
It solves a concrete business job with inputs and an observable output. It can be run in under two minutes with sensible defaults and one strong example.

## Lifecycle
Idea → Feasibility note → v0 (internal) → v1 (public) → Iterate or fold.

### Idea record (template)
```
Title: 
User Job: 
Inputs (shape): 
Output (shape): 
Evidence of demand: 
Nearest alt / how we differ: 
Next best action after output: 
Telemetry to add: 
```

### v1 shipping checklist
– One killer example prefilled.  
– Input validation and guardrails (no gotchas).  
– Plain-English model notes: strengths, blind spots.  
– “How this was made” link in the footer for trust.  
– Two deep links: a conceptual article and an operational guide.  
– Events wired (see `telemetry.md`).

## Page contract
Each tool page agrees to this layout and behaviour:

Header: title, 15-word promise, domain/capability badges.  
Form: minimal fields, one primary button.  
Result: clear output, copy/export, “what next” box.  
Side panel: Learn (2 links), Caveats, Feedback.  
Footer: version, last model update, “How this was made”.

### “What next” box (NBAs)
If simple outcome: invite to save, schedule, or subscribe to updates on this capability.  
If complex outcome detected: offer a consult link that preserves inputs.

## Monetisation
Free tier by default. Pro features include higher limits, bulk upload, API key, scheduled runs, and saved scenarios. Advisory upsell appears only when the tool’s outcome indicates material stakes.

## Quality bars
• Latency under 3s where feasible (show progress otherwise).  
• Deterministic formatting of outputs.  
• Zero empty states: show an example result if no user input yet.  
• Explain failure states (and how to fix them).

## Linking rules
Tools must link to at least one Knowledge article (concept) and one Guide (hands-on). Articles about a capability must surface the tool card inline at the first moment of practical application.

## Example: tool page skeleton (Django + template hints)
```html
<section class="tool" data-domain="{{ tool.domain }}" data-capability="{{ tool.capability }}">
  <header>
    <h1>{{ tool.title }}</h1>
    <p class="promise">{{ tool.promise }}</p>
  </header>
  <form id="tool-form" method="post">{% csrf_token %}
    {{ form|crispy }}
    <button class="btn btn-primary" data-analytics-event="tool_run">Run</button>
  </form>
  <div id="result" hidden>
    <pre>{{ result.rendered }}</pre>
    <div class="next">
      <h3>What next</h3>
      {% include "partials/nbas.html" with capability=tool.capability result=result %}
    </div>
  </div>
  <aside>
    {% include "partials/learn-more.html" with links=tool.learn_links %}
    {% include "partials/caveats.html" with caveats=tool.caveats %}
    {% include "partials/feedback.html" %}
  </aside>
  <footer>
    <small>v{{ tool.version }} · Model {{ tool.model_info }}</small>
    <a href="{% url 'article' tool.build_article_slug %}">How this was made</a>
  </footer>
</section>
```

## Back-office
Each tool keeps a short `docs/tools/<slug>.md` with: user job, inputs/outputs, edge cases, model notes, and change log. Keep it human.
