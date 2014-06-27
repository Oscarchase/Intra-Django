function add_to_group() {
    var user_login = $('#user_selection').val()

    if (group_members.length < group_size
        && group_members.indexOf(user_login) == -1)
    {
        $.ajax({
            url: '/profiles/picture/' + user_login,
            success: function(data) {
                $('#members-table > tbody').append(new_group_member_html(user_login, data))
                group_members.push(user_login)
            }
        })
    }
}

function remove_member(button, name) {
    var member_index = group_members.indexOf(name)

    group_members.splice(member_index, 1)
    $(button).parent().parent().remove()
}

function new_group_member_html(name, picture) {
    return '\
        <tr>\
          <td>\
            <span class="user-picture">' + picture + '</span>\
          </td>\
          <td>\
            <a href="/profiles/' + name + '" target="_blank">' + name + '</a>\
          </td>\
          <td>\
            <button type="button" class="close pull-right" onclick="remove_member(this, \'' + name + '\')">&times;</button>\
          </td>\
        </tr>\
    '
}

$(function() {
    $('#group-member-register').submit(function(event) {
        event.preventDefault();
        $.ajax({
            data: $(this).serialize() + '&group_members=' + JSON.stringify(group_members),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function(data) {
                $('#group-modal').modal('hide')
                window.location.reload()
            },
            error: function(data) {
                console.log(data.responseText)
            }
        });
    });
})
