<!-- allow: delegate screen capture / camera / mic to the frame, else a recorder
     inside it can never prompt (Permissions-Policy denies it silently). -->
<iframe src="{{ include.src }}" width="100%" 
  height="{{ include.height | default: 600 }}" 
  loading="lazy" allowfullscreen allow="display-capture; camera; microphone"
  style="border:none;"></iframe>
