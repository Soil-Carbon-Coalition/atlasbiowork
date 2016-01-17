requirejs.config({
    'baseUrl': '/js/lib',
    'paths': {
        'atlasbiowork': '../atlasbiowork',
        'data': '../data/'
    }
});

requirejs(['atlasbiowork/main']);
