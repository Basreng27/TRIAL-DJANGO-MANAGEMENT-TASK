var loading = `<div class="d-flex justify-content-center align-items-center" style="height: 100%;">
                    <div class="spinner-border" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>`;

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

$('.form-modal').on('click', function(){
    let url = $(this).data('url')

    $('#modal-form .modal-body').html(loading);

    $.ajax({
        url:url,
        method: 'GET',
        success: function(response) {
            $('#modal-form .modal-body').html(response);
            $('#modal-form').modal('show');
        },
        error: function() {
            Swal.fire({
                title: "Error",
                text: "Error loading form.",
                icon: "error"
            });
        },
        complete: function() {
            $('#modal-form .modal-body').find('.spinner-border').remove();
        }
    })
})

$('.save').on('click', function(event) {
    event.preventDefault();

    $('.save').prop('disabled', true);

    Swal.fire({
        title: "Are you sure ?",
        icon: "warning",
        showCancelButton: true,
        cancelButtonColor: "#d33",
        confirmButtonColor: "#3085d6",
        confirmButtonText: "Save"
    }).then((result) => {
        if (result.isConfirmed) {
            var form = $('#modal-form form')[0];
            var formData = new FormData(form);
            var url = $(form).attr('action');
            var csrfToken = getCookie('csrftoken');
            console.log(formData);
            console.log(url);

            $.ajax({
                url: url,
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                data: formData,
                processData: false,
                contentType: false,
                success: function(response) {
                    if (typeof response === 'string')
                        response = JSON.parse(response)

                    Swal.fire({
                        title: response.title,
                        text: response.message,
                        icon: response.icon
                    }).then(() => {
                        if (response.status)
                            window.location.href = response.redirect;
                    });
                },
                error: function() {
                    Swal.fire({
                        title: "Error",
                        text: "Error saving data.",
                        icon: "error"
                    });    
                },
                complete: function() {
                    $('.login').prop('disabled', false);
                }
            });
        }else{
            $('.login').prop('disabled', false);
        }
    });
})

$('.delete').on('click', function(event) {
    event.preventDefault();

    Swal.fire({
        title: "Are you sure delete data ?",
        icon: "warning",
        showCancelButton: true,
        cancelButtonColor: "#d33",
        confirmButtonColor: "#3085d6",
        confirmButtonText: "Yes"
    }).then((result) => {
        if (result.isConfirmed) {
            var url = $(this).data('url');
            var csrfToken = getCookie('csrftoken');

            $.ajax({
                url: url,
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrfToken  // Add CSRF token to header
                },
                success: function(response) {
                    Swal.fire({
                        title: response.title,
                        text: response.message,
                        icon: response.icon
                    }).then(() => {
                        if (response.status)
                            window.location.href = response.redirect;
                    });
                },
                error: function() {
                    Swal.fire({
                        title: "Error",
                        text: "Error delete data.",
                        icon: "error"
                    });    
                }
            });
        }
    });
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

function load_child(event){
    let element = event.currentTarget;
    let url = $(element).data('url');
    let parent = $(element).data('parent');
    let child_row = $(`#child-row-${parent}`);

    if (child_row.is(':visible')) {
        child_row.hide();
        
        return;
    }

    child_row.show();

    $(`#child-${parent}`).html(loading);

    $.ajax({
        url:url,
        method: 'GET',
        success: function(response) {
            $(`#child-${parent}`).html(response);
        },
        error: function() {
            Swal.fire({
                title: "Error",
                text: "Error loading form.",
                icon: "error"
            });
        },
        complete: function() {
            $(`#child-${parent}`).find('.spinner-border').remove();
        }
    })
}