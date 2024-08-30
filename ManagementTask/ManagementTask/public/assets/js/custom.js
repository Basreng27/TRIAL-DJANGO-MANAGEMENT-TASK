$(document).ready(function(){
    $('.login').on('click', function(e){
        e.preventDefault();

        $('.login').prop('disabled', true);

        var form = $('form')[0]
        var url = $(form).attr('action')
        var data = new FormData(form)
        var csrfToken = getCookie('csrftoken')
        
        $.ajax({
            url: url,
            method: 'POST',
            headers:{
                'X-CSRFToken': csrfToken
            },
            data: data,
            processData: false,
            contentType: false,
            success: function(response){
                if (typeof response === 'string')
                    response = JSON.parse(response)

                Swal.fire({
                    title: response.title,
                    text: response.message,
                    icon: 'success',
                }).then(() => {
                    if (response.status)
                        window.location.href = response.redirect
                })
            },
            error: function(){
                Swal.fire({
                    title: response.title,
                    text: response.message,
                    icon: 'error',
                })
            },
            complete: function() {
                $('.login').prop('disabled', false);
            }
        })
    })

    $('.logout').on('click', function(e){
        e.preventDefault();

        var url = $(this).attr('href')
        var csrfToken = getCookie('csrftoken')
        
        $.ajax({
            url: url,
            method: 'POST',
            headers:{
                'X-CSRFToken': csrfToken
            },
            success: function(response){
                if (typeof response === 'string')
                    response = JSON.parse(response)

                Swal.fire({
                    title: response.title,
                    text: response.message,
                    icon: 'success',
                }).then(() => {
                    if (response.status)
                        window.location.href = response.redirect
                })
            },
            error: function(){
                Swal.fire({
                    title: response.title,
                    text: response.message,
                    icon: 'error',
                })
            }
        })
    })
})

function getCookie(name){
    let cookieValue = null

    if (document.cookie && (document.cookie != '')){
        const cookies = document.cookie.split(';')

        for (let i = 0; i < cookies.length; i++){
            const cookie = cookies[i].trim()

            if (cookie.substring(0, name.length + 1) === (name + '=')){
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))

                break
            }
        }
    }

    return cookieValue
}