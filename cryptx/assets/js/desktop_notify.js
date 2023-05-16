
const site_image_url='https://content-terminal.cryptx.com/wp-content/uploads/2021/09/Cryptx-3.png';

function notify_on_desktop(msg) {
  if (!("Notification" in window)) {
    alert("This browser does not support desktop notification");
  }

  else if (Notification.permission === "granted") {
    var options = {
            body: msg,
            icon: site_image_url,
            dir : "ltr"
        };
    var notification = new Notification("Crypt-X",options);
  }

  else if (Notification.permission !== 'denied') {

    Notification.requestPermission(function (permission) {
      if (!('permission' in Notification))
      {
        Notification.permission = permission;
      }
      if (permission === "granted") {
        var options = {
              body: msg,
              icon: site_image_url,
              dir : "ltr"
          };
        var notification = new Notification("Hi there",options);
      }
    });
  }
}


