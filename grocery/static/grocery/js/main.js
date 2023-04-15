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
  var $loadingframe = $("#loading-frame");
  var $submit = $("input[type='submit']");
  var $select = $("#select-units");
  var $form_submit = $("#form-result");
  var $img_result = $("#img-result")
  var $img_result_container = $("#img-result-container");

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
          $submit.prop("disabled", false);
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

    if (!cropper) {
      return;
    }

    cropper.getCroppedCanvas().toBlob(function (blob) {

      $loadingframe.removeClass("d-none");
      var body = document.getElementsByTagName("body")[0];
      $(body).addClass("loading");

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
          // $result.removeClass("d-none");

          // ok 
          cropper.destroy();
          image.src = ''; // '/grocery/ticket_tmp/tiquet.jpg';
          $loadingframe.addClass("d-none");
          $submit.prop("disabled", true);


          var out = "<div><br></div>";
          $.each(e.items_processed.productes, function (i, v) {
            var select = $select[0].outerHTML;


            out += "<div class='row-producto row mb-1'>"
            out += "<div class='col-12'><label>" + v.producte + "</label></div>";
            out += "<div class='col-9 mb-2 mb-md-0 col-md-6'><input title='Producte' class='form-control' type='text' name='producte[" + i + "][name]' value='" + v.nom_simplificat + "'/></div>"
            out += "<div class='col-3 mb-2 mb-md-0 col-md-2 with-label'><label>#</label><input title='Quantitat' class='form-control' type='number' name='producte[" + i + "][amount]' value='" + v.quantitat + "'/></div>"
            out += "<div class='col-5 col-md-2'>" + select.replace('name=""', 'name="producte[' + i + '][unit]"') + "</div>"
            out += "<div class='col-4 col-md-2 with-label'><label>€</label><input title='Preu' class='form-control' type='text' name='producte[" + i + "][price]' value='" + v.preu + "'/></div>"
            out += "</div>";
          });

          $form_submit.removeClass("d-none");
          $form_submit.append($(out));
          $form_submit.after($("<input type='submit' class='mt-3 btn btn-sm btn-success mt-3' value='Desa els productes'/>"));

          $img_result_container.removeClass("d-none");
          // $img_result.removeClass("d-none");

          $(body).removeClass("loading");



        },
        error: function (e) {
          $error.html(e.error_message);
          $loadingframe.addClass("d-none");

          $(body).removeClass("loading");


        },
      });
    });

  })


};
