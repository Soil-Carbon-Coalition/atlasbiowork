define(["data/config", "data/templates", "data/version"],
function(config, templates, version) {

config.router = {
    'base_url': ''
}

config.template = {
    'templates': templates,
    'defaults': {
        'version': version,
        'obs_html': function() {
            return function(text, render) {
                return render(this.type[text + '_html']);
            }
        },
        'selected': function() {
            return function(text, render) {
                var parts = text.split(' ');
                if (this[parts[0]] === parts[1]) {
                    return ' checked';
                }
                return '';
            }
        }
    }
};

config.store = {
    'service': config.router.base_url,
    'defaults': {'format': 'json'}
}

config.map = {
    'bounds': [[44.7, -93.6], [45.2, -92.8]]
};

config.outbox = {};

config.transitions = {
    'default': "slide",
    'save': "flip"
};

config.pages.site.map.list.onshow = function(map) {
    map.locate({
        'setView': true,
        'maxZoom': 16,
    });
}

return config;

});
