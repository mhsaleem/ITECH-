/**
 * Created by rorybain on 08/03/2016.
 */
jQuery(document).ready(function($) {

    /**
     * Example 1
     * Load from SELECT field
     */
    $('#e1_element').fontIconPicker();
    var notification = $('#virginbox');
    msg = $.cookie('virgin');
    if (msg) {
        notification.show();
        notification.text('Thanks for signing up! If you want you can customize your profile here. Your title will be displayed next to any puns you post, earn new ones by posting puns!')
    }

    saved_msg = $.cookie('saved');
    if (saved_msg) {
        notification.show();
        notification.text('Your details have been saved!');
    }


});