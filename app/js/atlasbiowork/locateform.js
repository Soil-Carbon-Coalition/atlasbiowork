define(['wq/template'], function(tmpl) {
    return {
        'name': 'locateform',
        'init': function() {},
        'run': function($page, routeInfo) {
            if (routeInfo.page != 'locate') {
                return;
            }
            // On locate form submission:
            //  - store site as template variable for use in observations/new
            //  - navigate to observation type list
            var $form = $page.find('form'), app=this.app;
            $form.on('submit', function(evt) {
                var site = {};
                $form.serializeArray().forEach(function(field) {
                    site[field.name] = field.value;
                });
                tmpl.setDefault('site_data', JSON.stringify(site));
                tmpl.setDefault('site_data_label', tmpl.render(
                      "{{name}} ({{latitude}}, {{longitude}})",
                      site
                ));
                app.go('observationtype', 'list');
            });
        }
    };
})
