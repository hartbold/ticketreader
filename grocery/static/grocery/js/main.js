var cropper;

window.onload = function () {
  'use strict';

  var Cropper = window.Cropper;
  var URL = window.URL || window.webkitURL;
  var container = document.querySelector('.img-container');
  var image = container.getElementsByTagName('img').item(0);
  var uploadedImageType = 'image/jpeg';
  var uploadedImageName = 'cropped.jpg';
  var uploadedImageURL;
  var $error = $("#error");
  var $result = $("#result");

  // Import image
  var inputImage = document.getElementById('inputImage');

  if (URL) {
    inputImage.onchange = function () {
      var files = this.files;
      var file;

      if (files && files.length) {
        file = files[0];

        if (/^image\/\w+/.test(file.type)) {
          uploadedImageType = file.type;
          uploadedImageName = file.name;

          if (uploadedImageURL) {
            URL.revokeObjectURL(uploadedImageURL);
          }

          image.src = uploadedImageURL = URL.createObjectURL(file);

          if (cropper) {
            cropper.destroy();
          }

          cropper = new Cropper(image, {
            'viewMode': 2,
            'movable': false,
            'rotatable': false,
            'scalable': false,
            'zoomable': false,
          });
          inputImage.value = null;
        } else {
          window.alert('Please choose an image file.');
        }
      }
    };
  } else {
    inputImage.disabled = true;
    inputImage.parentNode.className += ' disabled';
  }

  if (!HTMLCanvasElement.prototype.toBlob) {
    Object.defineProperty(HTMLCanvasElement.prototype, 'toBlob', {
      value: function (callback, type, quality) {
        var canvas = this;
        setTimeout(function () {
          var binStr = atob(canvas.toDataURL(type, quality).split(',')[1]),
            len = binStr.length,
            arr = new Uint8Array(len);

          for (var i = 0; i < len; i++) {
            arr[i] = binStr.charCodeAt(i);
          }

          callback(new Blob([arr], { type: type || 'image/png' }));
        });
      }
    });
  }

  document.getElementById("form").addEventListener("submit", function (e) {
    e.preventDefault();
    cropper.getCroppedCanvas().toBlob(function (blob) {
      var formData = new FormData();
      formData.append('croppedImage', new File([blob], 'tiquet.jpg', { type: 'image/jpeg' }));
      formData.append('csrfmiddlewaretoken', document.getElementsByName("csrfmiddlewaretoken")[0].value)
      // Use `jQuery.ajax` method
      $.ajax('upload', {
        method: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function (e) {

          $result.html(e.error_message);
          $result.val(e.error_message);
          $result.removeClass("d-none");

          // ok 
          cropper.destroy();
          image.src = '';

        },
        error: function (e) {
          $error.html(e.error_message);
        }
      });
    });

  })


};
