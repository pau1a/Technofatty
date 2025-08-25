import json
import subprocess
import tempfile
import textwrap

from django.test import TestCase


class PrimaryNavA11yTests(TestCase):
    def test_primary_nav_attributes_and_keyboard(self):
        response = self.client.get('/')
        self.assertContains(response, 'id="primary-nav"')
        self.assertContains(response, 'aria-controls="primary-nav"')
        html = response.content.decode()

        subprocess.run(
            ['npm', 'install', 'jsdom@22', '--no-save', '--no-package-lock'],
            check=True,
            stdout=subprocess.DEVNULL,
        )

        with tempfile.NamedTemporaryFile('w', suffix='.html') as html_file, tempfile.NamedTemporaryFile('w', suffix='.js') as script_file:
            html_file.write(html)
            html_file.flush()
            script_file.write(textwrap.dedent(
                """
                const fs = require('fs');
                const {JSDOM} = require('jsdom');
                const html = fs.readFileSync(process.argv[2], 'utf8');
                const main = fs.readFileSync(process.argv[3], 'utf8');
                const dom = new JSDOM(html, { runScripts: 'outside-only' });
                const { window } = dom;
                window.requestAnimationFrame = cb => cb();
                window.matchMedia = () => ({ matches: false, addEventListener: () => {}, removeEventListener: () => {} });
                window.eval(main);
                window.document.dispatchEvent(new window.Event('DOMContentLoaded', { bubbles: true }));
                const button = window.document.querySelector('.hamburger-btn');
                const nav = window.document.getElementById('primary-nav');
                const focusables = nav.querySelectorAll('a, button');
                const first = focusables[0];
                const last = focusables[focusables.length - 1];
                function state() {
                  return { expanded: button.getAttribute('aria-expanded'), hidden: nav.getAttribute('aria-hidden'), active: window.document.activeElement === first };
                }
                console.log(JSON.stringify(state()));
                button.dispatchEvent(new window.Event('click', { bubbles: true }));
                console.log(JSON.stringify(state()));
                last.focus();
                nav.dispatchEvent(new window.KeyboardEvent('keydown', { key: 'Tab', bubbles: true }));
                console.log(JSON.stringify(state()));
                nav.dispatchEvent(new window.KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
                console.log(JSON.stringify(state()));
                """
            ))
            script_file.flush()
            result = subprocess.run(
                ['node', script_file.name, html_file.name, 'coresite/static/coresite/js/main.js'],
                capture_output=True,
                text=True,
                check=True,
            )

        states = [json.loads(line) for line in result.stdout.strip().splitlines()]
        initial, after_click, after_tab, after_escape = states
        self.assertEqual(initial['expanded'], 'false')
        self.assertEqual(after_click['expanded'], 'true')
        self.assertTrue(after_tab['active'])
        self.assertEqual(after_escape['expanded'], 'false')
