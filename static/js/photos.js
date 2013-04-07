$(document).ready(function(){
    _.each(values, function(val, name) {
        $('input[name="'+name+'"],textarea[name="'+name+'"]').val(val);     
    });
    $('.control-group.error').on('change keyup', function() {
        $(this).removeClass('error');
    });
    $('#shadow').on('click', function() {
        $('.snapshot-detail').addClass('hide');
        $('#shadow').addClass('hide');
    });
    $('.snapshot').on('click', function() {
        var pid = $(this).data('pid');
        $('.snapshot-detail[data-pid="'+pid+'"]').removeClass('hide');
        $('#shadow').removeClass('hide').height($(document).height());
    });
    $('input[type=text],input[type=password]').on('keydown', function(ev) {
        if (ev.which == 13) {
            console.log('got enter key', ev);
            ev.preventDefault();
            ev.stopPropagation();
            $('input[type=submit]').trigger('click');
        }
    });

});
