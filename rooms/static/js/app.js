$(function() {
    var $from = $('#unit-from'),
        $name = $('#name'),
        $size = $('#size'),
        $calculate = $('#calculate'),
        $submit = $('#submit'),
        $results = $('#results');

    var getUnitData = function() {
        return {size: $size.val()};
    };

    var renderResults = function(results) {
        var $ul = $('<ul>');
        $.each(results, function(room) {
            var $li = $('<li>');
            $li.text('room size here');
            $ul.append($li);
        });
        $results.html($ul);
    };

    var calculate = function(e) {
        e.preventDefault();
        $.getJSON('/units/calculate', getUnitData(), renderResults);
    };

    $('#calculate').on('click', calculate);
});

