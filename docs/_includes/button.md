<style>
.button { display: inline-block; padding: 0.5em 1.2em; background: #0066cc; color: white !important; text-decoration: none !important; border-radius: 4px; font-weight: 600; transition: background 0.15s; margin: 0.2em 0.3em 0.2em 0; }
.button:hover { background: #0052a3; }
.button-secondary { background: #6c757d; }
.button-secondary:hover { background: #5a6268; }
.button-success { background: #28a745; }
.button-success:hover { background: #1e7e34; }
.button-danger { background: #dc3545; }
.button-danger:hover { background: #bd2130; }
.button-outline { background: transparent; color: #0066cc !important; border: 2px solid #0066cc; padding: calc(0.5em - 2px) calc(1.2em - 2px); }
.button-outline:hover { background: #0066cc; color: white !important; }
</style>
<a href="{{ include.href }}" class="button{% if include.style %} button-{{ include.style }}{% endif %}">{{ include.label }}</a>
