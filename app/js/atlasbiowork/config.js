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

var attrib = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>';
var mapbox = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}';

// Map defaults
config.map = {
    'bounds': [[49, -122], [25, -66]],
    'basemaps': [{
        'name': 'MapBox Satellite',
        'type': 'tile',
        'url': mapbox,
        'id': 'mapbox.satellite',
        'accessToken': config.mapbox_token,
        'attribution': attrib
    }, {
        'name': 'MapBox Streets',
        'type': 'tile',
        'url': mapbox,
        'id': 'mapbox.streets',
        'accessToken': config.mapbox_token,
        'attribution': attrib
    }]
};


config.outbox = {};

config.transitions = {
    'default': "slide",
    'save': "flip"
};

config.pages.site.map.forEach(function(mconf) {
    if (mconf.mode == 'list') {
        mconf.onshow = function(map) {
	    map.locate({
		'setView': true,
		'maxZoom': 16,
	    });
        };
    }
});

return config;

});
