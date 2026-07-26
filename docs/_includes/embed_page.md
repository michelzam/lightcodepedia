<!-- allow: an embedded LC page carries the same components as a standalone one —
     the recorder needs display-capture (and camera/mic) delegated by THIS frame,
     or the browser never even prompts and the record button looks dead. -->
<iframe src="{{ include.page }}?embed=true" width="100%" height="{{ include.height | default: 400 }}" loading="lazy" allow="display-capture; camera; microphone" style="border:none;"></iframe>
