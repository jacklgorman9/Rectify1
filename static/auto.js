$(function() {
    $.ajax({
        url: '{{ url_for("autocomplete") }}'
        }).done(function (data){
            $('#city_autocomplete').autocomplete({
                source: data,
                minLength: 2
            });
        });
    });
