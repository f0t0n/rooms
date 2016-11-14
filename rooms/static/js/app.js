$(function() {
    var $form = $('#unit-from'),
        $name = $('#name'),
        $width = $('#width'),
        $length = $('#length'),
        $calculate = $('#calculate'),
        $submit = $('#submit'),
        $results = $('#results')
        rooms = null;

    var getUnitData = function() {
        return {name: $name.val(), width: $width.val(), length: $length.val()};
    };


    var createList = function(items) {
        var $ul = $('<ul>');
        $.each(items, function(i, item) {
            var $li = $('<li>');
            $li.text(item);
            $ul.append($li);
        });
        return $ul;
    };

    var renderResults = function(results) {
        rooms = results;
        var items = $.map(results, function(item) {
            return item[0] + 'x' + item[1];
        });
        $results.html(createList(items));
    };

    var renderError = function(jqXHR, textStatus, errorThrown) {
        $results.html(createList([errorThrown]));
    };

    var calculate = function(e) {
        e.preventDefault();
        rooms = null;
        $.getJSON('/units/calculate', getUnitData())
            .done(renderResults)
            .fail(renderError);
    };

    var saveUnit = function(e) {
        e.preventDefault();
        if(! rooms) {
            alert('Please calculate first.');
            return false;
        }
        unitData = getUnitData();
        unitData.rooms = rooms;
        $.ajax({
            url: '/units',
            type: 'POST',
            data: JSON.stringify(unitData),
            contentType: 'application/json',
            dataType: 'json',
            success: function(unit) {
                rooms = null;
                window.location.href = '/units';
            },
            error: function(jqXHR, testStatus, errorThrown) {
                alert(errorThrown);
            }
        });
    };

    $('#calculate').on('click', calculate);

    $submit.on('click', saveUnit);
});

