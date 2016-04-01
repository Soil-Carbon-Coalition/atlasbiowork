// Dynamically add nested observation records to form
// c.f. wq/patterns.js

define(['jquery', 'wq/template'], function($, tmpl) {
return {
    'init': function() {},
    'run': function($page) {
        var model = this.app.models.observationtype;
        var $buttons = $page.find('button[data-atlas-action=addobs]');
        var typeId = $page.find('[name=type_id]').val();

        model.find(typeId).then(function(type) {
            $buttons.on('click', function(evt) {
                var $button = $(evt.target),
                    section = $button.data('atlas-section'),
                    count = $page.find('.section-' + section).length,
                    pattern = '{{#' + section + '}}([\\s\\S]+){{/' + section + '}}',
                    match = type.edit_html.match(pattern),
                    $obs = $(tmpl.render(match[1], {
                        '@index': count
                    }));
                $button.parents('li').before($obs);
                $obs.enhanceWithin();
                $button.parents('ul').listview('refresh');
            });
        });
    }
};

});
