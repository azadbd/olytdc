function enbleDisableExt()
    {
    var radios = document.querySelector('input[name="audio-video"]:checked').value;
    console.log("radios: "+radios);
             if (radios==='A')
                 {
                     var v = document.getElementById("video-ext");
                     var a = document.getElementById("audio-ext");
                     v.className += " disabled";
                     a.classList.remove("disabled");
                  }

             else {
                    var v = document.getElementById("video-ext");
                    var a = document.getElementById("audio-ext");
                    v.classList.remove("disabled");
                    a.className += " disabled";
                  }
     }
