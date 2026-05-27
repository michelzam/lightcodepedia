<style>
.lc-btn { display: inline-block; padding: 0.5em 1.2em; background: #0066cc; color: white !important; text-decoration: none !important; border-radius: 4px; font-weight: 600; transition: background 0.15s; margin: 0.2em 0.3em 0.2em 0; }
.lc-btn:hover { background: #0052a3; }
.lc-btn-secondary { background: #6c757d; }
.lc-btn-secondary:hover { background: #5a6268; }
.lc-btn-success { background: #28a745; }
.lc-btn-success:hover { background: #1e7e34; }
.lc-btn-danger { background: #dc3545; }
.lc-btn-danger:hover { background: #bd2130; }
.lc-btn-outline { background: transparent; color: #0066cc !important; border: 2px solid #0066cc; padding: calc(0.5em - 2px) calc(1.2em - 2px); }
.lc-btn-outline:hover { background: #0066cc; color: white !important; }
</style>
<a href="{{ include.href }}" class="lc-btn{% if include.style %} lc-btn-{{ include.style }}{% endif %}">{{ include.label }}</a>
