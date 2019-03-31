




/*Ajax--------------------------------------------------------------------------*/
function _sendAjax(data, words){

    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();


    $.ajax({
        type: "POST",
        url: "ajax/",
        data: data,
        cache: false,

        success: function (data) {
            console.log(data);
            document.location.href = "{% url 'tests' %}";
        },

        error: function (request, error) {
            console.log(error + request.status + request.statusText);
        },

        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
    });
};