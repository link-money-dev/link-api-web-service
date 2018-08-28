(function ($) {
    'use strict';
    $(document)['ready'](function () {
        _0x2f2exe();
        if ($('.menu-trigger')['length']) {
            $('.menu-trigger')['click'](function () {
                $(this)['toggleClass']('active');
                $('.header-area .nav')['slideToggle'](200)
            })
        };
        $('body')['click'](function (_0x2f2ex4) {
            var _0x2f2ex5 = _0x2f2ex4['target'];
            if ($(_0x2f2ex5)['parents']('.flag-list')['length'] || $(_0x2f2ex5)['hasClass']('flag-list')) {
                return
            };
            if ($('.flag-list')['css']('display') === 'block') {
                $('.flag-list')['css']('display', 'none');
                return
            };
            if ($(_0x2f2ex5)['hasClass']('selected') || $(_0x2f2ex5)['parents']('.selected')['length']) {
                $('.flag-list')['css']('display', 'block')
            }
        });
        if ($('.countdown')['length']) {
            $('.countdown')['downCount']({
                date: '09/29/2018 12:00:00',
                offset: +10
            })
        };
        if ($('.token .token-input')['length']) {
            $('.token .token-input .fa-plus')['click'](function () {
                var _0x2f2ex6 = $(this)['parent']()['find']('input')['val']();
                var _0x2f2ex7 = $(this)['parent']()['find']('input')['data']('step');
                if (_0x2f2ex6 == '') {
                    _0x2f2ex6 = 0
                };
                var _0x2f2ex8 = parseInt(_0x2f2ex6, 10) + parseInt(_0x2f2ex7, 10);
                $(this)['parent']()['find']('input')['val'](_0x2f2ex8)
            });
            $('.token .token-input .fa-minus')['click'](function () {
                var _0x2f2ex6 = $(this)['parent']()['find']('input')['val']();
                var _0x2f2ex7 = $(this)['parent']()['find']('input')['data']('step');
                if (_0x2f2ex6 == '') {
                    _0x2f2ex6 = 0
                };
                var _0x2f2ex8 = parseInt(_0x2f2ex6, 10) - parseInt(_0x2f2ex7, 10);
                if (_0x2f2ex8 <= 0) {
                    _0x2f2ex8 = _0x2f2ex7
                };
                $(this)['parent']()['find']('input')['val'](_0x2f2ex8)
            })
        };
        window['sr'] = new scrollReveal();
        $('a[href*=\#]:not([href=\#])')['click'](function () {
            // if (location['pathname']['replace'](/^\//, '') == this['pathname']['replace'](/^\//, '') && location['hostname'] == this['hostname']) {
                
                var _0x2f2ex9 = $(this['hash']);
                _0x2f2ex9 = _0x2f2ex9['length'] ? _0x2f2ex9 : $('[name=' + this['hash']['slice'](1) + ']');
                if (_0x2f2ex9['length']) {
                    var _0x2f2exa = $(window)['width']();
                    if (_0x2f2exa < 991) {
                        $('.menu-trigger')['removeClass']('active');
                        $('.header-area .nav')['slideUp'](200)
                    };
                    $('html,body')['animate']({
                        scrollTop: (_0x2f2ex9['offset']()['top']) - 30
                    }, 700);
                    return false
                }
            // }
        });
        if ($('.token-progress ul')['length']) {
            $('.token-progress ul')['find']('.item')['each'](function (_0x2f2exb) {
                $('.token-progress ul .item:eq(' + [_0x2f2exb] + ')')['css']('left', $('.token-progress ul .item:eq(' + [_0x2f2exb] + ')')['data']('position'))
            });
            var _0x2f2exc = $('.token-progress ul .progress-active')['data']('progress');
            $('.token-progress ul .progress-active')['css']('width', _0x2f2exc)
        };
        if ($('.table-progress')['length']) {
            $('.table-latests')['find']('.table-progress')['each'](function (_0x2f2exb) {
                $('.table-progress:eq(' + [_0x2f2exb] + ') .progress-line')['css']('width', parseInt($('.table-progress:eq(' + [_0x2f2exb] + ') .progress-line')['data']('value'), 10) + parseInt(70, 10) + '%')
            })
        };
        if ($('.roadmap-modern-wrapper')['length']) {
            $('.roadmap-modern-wrapper')['owlCarousel']({
                loop: true,
                margin: 30,
                nav: false,
                responsive: {
                    0: {
                        items: 1
                    },
                    600: {
                        items: 2
                    },
                    1000: {
                        items: 3
                    }
                }
            })
        };
        if ($('.roadmap-lux-wrapper')['length']) {
            $('.roadmap-lux-wrapper')['owlCarousel']({
                loop: true,
                margin: 30,
                nav: false,
                responsive: {
                    0: {
                        items: 1
                    },
                    600: {
                        items: 2
                    },
                    1000: {
                        items: 3
                    }
                }
            })
        }
    });
    $(window)['load'](function () {
        $('.loading-wrapper')['animate']({
            "\x6F\x70\x61\x63\x69\x74\x79": '0'
        }, 600, function () {
            setTimeout(function () {
                $('.loading-wrapper')['css']('visibility', 'hidden')['fadeOut']();
                if ($('.parallax')['length']) {
                    $('.parallax')['parallax']({
                        imageSrc: 'assets/images/parallax.jpg',
                        zIndex: '1'
                    })
                }
            }, 300)
        })
    });
    $(window)['scroll'](function () {
        var _0x2f2exa = $(window)['width']();
        if (_0x2f2exa > 991) {
            var _0x2f2exd = $(window)['scrollTop']();
            if (_0x2f2exd >= 30) {
                $('.header-area')['addClass']('header-sticky');
                $('.header-area .dark-logo')['css']('display', 'block');
                $('.header-area .light-logo')['css']('display', 'none')
            } else {
                $('.header-area')['removeClass']('header-sticky');
                $('.header-area .dark-logo')['css']('display', 'none');
                $('.header-area .light-logo')['css']('display', 'block')
            }
        }
    });
    $(window)['resize'](function () {
        _0x2f2exe()
    });

    function _0x2f2exe() {
        var _0x2f2exa = $(window)['width']();
        if (_0x2f2exa > 991) {
            var _0x2f2exf = $(window)['height']();
            $('.welcome-area')['css']('height', _0x2f2exf - 80)
        } else {
            $('.welcome-area')['css']('height', 'auto')
        };
        if ($('#welcome-1')['length']) {
            particlesJS('welcome-1', welcome1Settings)
        }
    }
})(jQuery)