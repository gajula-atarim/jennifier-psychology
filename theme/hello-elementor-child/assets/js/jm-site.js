/* Jennifer Malecki — small front-end behaviours for the Elementor build. */
( function () {
	'use strict';

	var reduceMotion = false;
	try {
		reduceMotion = window.matchMedia( '(prefers-reduced-motion: reduce)' ).matches;
	} catch ( e ) {}

	// "Take a breath with the ocean": the button widget with class jm-breath-toggle
	// starts and pauses the wave in the same section.
	function initBreath( toggle ) {
		var scope = toggle.closest( '.jm-breathe' ) || document;
		var breath = scope.querySelector( '.jm-breath' );
		var button = toggle.querySelector( '.elementor-button' );
		var label = toggle.querySelector( '.elementor-button-text' );
		if ( ! breath || ! button ) {
			return;
		}

		button.setAttribute( 'role', 'button' );
		button.setAttribute( 'tabindex', '0' );

		function set( running ) {
			breath.classList.toggle( 'is-running', running );
			breath.classList.toggle( 'is-paused', ! running );
			button.setAttribute( 'aria-pressed', running ? 'true' : 'false' );
			if ( label ) {
				label.textContent = running ? 'Pause' : 'Start breathing';
			}
		}

		// Restart the wave and both words on the same frame, so every start
		// begins with a full "Breathe in" as the wave rises.
		var phased = breath.querySelectorAll( '.jm-breath-rise, .jm-b-in, .jm-b-out' );
		function restart() {
			phased.forEach( function ( el ) {
				el.style.animation = 'none';
			} );
			void breath.offsetWidth;
			phased.forEach( function ( el ) {
				el.style.animation = '';
			} );
		}

		set( ! reduceMotion );

		button.addEventListener( 'click', function ( event ) {
			event.preventDefault();
			var start = ! breath.classList.contains( 'is-running' );
			if ( start ) {
				restart();
			}
			set( start );
		} );
		button.addEventListener( 'keydown', function ( event ) {
			if ( ' ' === event.key || 'Enter' === event.key ) {
				event.preventDefault();
				button.click();
			}
		} );
	}

	// Keep the hero video playing muted and inline (iOS needs both set before play()).
	function initHeroVideo( video ) {
		video.muted = true;
		video.playsInline = true;
		video.setAttribute( 'playsinline', '' );
		var attempt = function () {
			if ( video.paused && video.play ) {
				var played = video.play();
				if ( played && played.catch ) {
					played.catch( function () {} );
				}
			}
		};
		video.addEventListener( 'loadedmetadata', attempt );
		video.addEventListener( 'canplay', attempt );
		attempt();
	}

	// "Your next step": hold the footprint walk until the steps scroll into view, so every
	// visitor sees it begin at step 01. Without this script the walk simply runs from page load.
	function initFootprints() {
		var rows = document.querySelectorAll( '.jm-steps' );
		if ( ! rows.length ) {
			return;
		}
		rows.forEach( function ( row ) {
			row.classList.add( 'jm-walk-pending' );
		} );
		if ( ! ( 'IntersectionObserver' in window ) ) {
			rows.forEach( function ( row ) {
				row.classList.remove( 'jm-walk-pending' );
			} );
			return;
		}
		var observer = new IntersectionObserver( function ( entries ) {
			entries.forEach( function ( entry ) {
				if ( entry.isIntersecting ) {
					entry.target.classList.remove( 'jm-walk-pending' );
					observer.unobserve( entry.target );
				}
			} );
		}, { threshold: 0.35 } );
		rows.forEach( function ( row ) {
			observer.observe( row );
		} );
	}

	// Pop-ups: any link to "#jm-pop-…" opens the matching hidden container as a modal dialog.
	function initModals() {
		var modals = document.querySelectorAll( '.jm-modal' );
		if ( ! modals.length || document.body.classList.contains( 'elementor-editor-active' ) ) {
			return;
		}
		var lastFocus = null;
		modals.forEach( function ( modal ) {
			// Leave the pop-up where Elementor placed it (a top-level container): Elementor's own styles
			// for it (panel colour, padding, fonts) only apply inside the page's wrapper.
			var panel = modal.querySelector( '.jm-modal-panel' ) || modal;
			var title = modal.querySelector( '.jm-modal-title .elementor-heading-title' );
			panel.setAttribute( 'role', 'dialog' );
			panel.setAttribute( 'aria-modal', 'true' );
			panel.setAttribute( 'tabindex', '-1' );
			if ( title ) {
				title.id = title.id || ( modal.id || 'jm-pop' ) + '-label';
				panel.setAttribute( 'aria-labelledby', title.id );
			}
			modal.addEventListener( 'click', function ( event ) {
				if ( event.target === modal || event.target.closest( '.jm-modal-close' ) ) {
					close( modal );
				}
			} );
		} );

		function find( id ) {
			return document.getElementById( id ) || document.querySelector( '.jm-modal.' + id );
		}
		function open( modal ) {
			lastFocus = document.activeElement;
			modal.classList.add( 'is-open' );
			document.body.classList.add( 'jm-modal-open' );
			var panel = modal.querySelector( '.jm-modal-panel' ) || modal;
			panel.focus();
		}
		function close( modal ) {
			modal.classList.remove( 'is-open' );
			document.body.classList.remove( 'jm-modal-open' );
			if ( lastFocus && lastFocus.focus ) {
				lastFocus.focus();
			}
		}

		document.addEventListener( 'click', function ( event ) {
			var a = event.target.closest( 'a[href*="#jm-pop-"]' );
			if ( ! a ) {
				return;
			}
			var modal = find( a.getAttribute( 'href' ).split( '#' )[ 1 ] );
			if ( modal ) {
				event.preventDefault();
				open( modal );
			}
		} );
		document.addEventListener( 'keydown', function ( event ) {
			var openModal = document.querySelector( '.jm-modal.is-open' );
			if ( ! openModal ) {
				return;
			}
			if ( 'Escape' === event.key ) {
				close( openModal );
			} else if ( 'Tab' === event.key ) {
				var items = openModal.querySelectorAll( 'a[href], button, [tabindex]:not([tabindex="-1"])' );
				if ( ! items.length ) {
					return;
				}
				var first = items[ 0 ], last = items[ items.length - 1 ];
				if ( event.shiftKey && document.activeElement === first ) {
					event.preventDefault();
					last.focus();
				} else if ( ! event.shiftKey && document.activeElement === last ) {
					event.preventDefault();
					first.focus();
				}
			}
		} );
		// Open straight away when the page is loaded with a pop-up's address (e.g. /#jm-pop-fees).
		if ( location.hash.indexOf( '#jm-pop-' ) === 0 ) {
			var initial = find( location.hash.slice( 1 ) );
			if ( initial ) {
				open( initial );
			}
		}
	}

	// Menu button on desktop: UAE only opens its menu below 1025px, so above that we open and close
	// the same menu ourselves (the panel styling is in jm-site.css).
	function initDesktopMenu() {
		var navs = document.querySelectorAll( '.jm-nav' );
		var desktop = window.matchMedia( '(min-width: 1025px)' );
		navs.forEach( function ( nav ) {
			var toggle = nav.querySelector( '.hfe-nav-menu__toggle' );
			if ( ! toggle ) {
				return;
			}
			toggle.setAttribute( 'role', 'button' );
			toggle.setAttribute( 'tabindex', '0' );
			toggle.setAttribute( 'aria-label', 'Menu' );
			function set( open ) {
				nav.classList.toggle( 'jm-menu-open', open );
				toggle.setAttribute( 'aria-expanded', open ? 'true' : 'false' );
			}
			set( false );
			toggle.addEventListener( 'click', function ( event ) {
				if ( ! desktop.matches ) {
					return;
				}
				event.preventDefault();
				event.stopImmediatePropagation();
				set( ! nav.classList.contains( 'jm-menu-open' ) );
			}, true );
			toggle.addEventListener( 'keydown', function ( event ) {
				if ( desktop.matches && ( 'Enter' === event.key || ' ' === event.key ) ) {
					event.preventDefault();
					set( ! nav.classList.contains( 'jm-menu-open' ) );
				}
			} );
			document.addEventListener( 'click', function ( event ) {
				if ( nav.classList.contains( 'jm-menu-open' ) && ! nav.contains( event.target ) ) {
					set( false );
				}
			} );
			document.addEventListener( 'keydown', function ( event ) {
				if ( 'Escape' === event.key && nav.classList.contains( 'jm-menu-open' ) ) {
					set( false );
					toggle.focus();
				}
			} );
			desktop.addEventListener( 'change', function () {
				set( false );
			} );
		} );
	}

	// Gallery: filter chips, a lightbox with previous/next, and no right-click saving of the artwork.
	function initGallery() {
		var items = Array.prototype.slice.call( document.querySelectorAll( '.jm-g-item' ) );
		document.addEventListener( 'contextmenu', function ( event ) {
			if ( event.target.closest( '.jm-figure, .jm-g-img, .jm-art, .jm-lightbox' ) ) {
				event.preventDefault();
			}
		} );
		if ( ! items.length ) {
			return;
		}
		var filters = document.querySelectorAll( '.jm-filters:not(.jm-res-filters) .jm-filter' );
		filters.forEach( function ( btn ) {
			btn.addEventListener( 'click', function () {
				var f = btn.getAttribute( 'data-filter' );
				filters.forEach( function ( b ) {
					b.setAttribute( 'aria-pressed', b === btn ? 'true' : 'false' );
				} );
				items.forEach( function ( it ) {
					it.classList.toggle( 'is-hidden', 'all' !== f && ! it.classList.contains( 'jm-g-' + f ) );
				} );
			} );
		} );

		function text( it, sel ) {
			var el = it.querySelector( sel + ' .elementor-heading-title' );
			return el ? el.textContent.trim() : '';
		}
		function viewable() {
			return items.filter( function ( it ) {
				return ! it.classList.contains( 'is-hidden' ) && it.querySelector( '.jm-g-img img' );
			} );
		}
		var box = null, index = 0, list = [], lastFocus = null;
		function show() {
			var it = list[ index ], img = it.querySelector( '.jm-g-img img' );
			box.querySelector( 'img' ).src = img.currentSrc || img.src;
			box.querySelector( 'img' ).alt = img.alt;
			box.querySelector( '.jm-lb-text' ).innerHTML = '<strong></strong> · <span></span> · © Jennifer Malecki';
			box.querySelector( '.jm-lb-text strong' ).textContent = text( it, '.jm-g-title' );
			box.querySelector( '.jm-lb-text span' ).textContent = text( it, '.jm-g-kind' );
			box.setAttribute( 'aria-label', text( it, '.jm-g-title' ) );
		}
		function close() {
			if ( box ) {
				box.remove();
				box = null;
				document.body.classList.remove( 'jm-modal-open' );
				if ( lastFocus ) {
					lastFocus.focus();
				}
			}
		}
		function open( it ) {
			list = viewable();
			index = Math.max( 0, list.indexOf( it ) );
			lastFocus = document.activeElement;
			var btn = function ( cls, label, path ) {
				return '<button type="button" class="jm-round jm-round-light ' + cls + '" aria-label="' + label + '">' +
					'<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="' + path + '" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>';
			};
			box = document.createElement( 'div' );
			box.className = 'jm-lightbox';
			box.setAttribute( 'role', 'dialog' );
			box.setAttribute( 'aria-modal', 'true' );
			box.innerHTML = '<figure><img alt="" draggable="false"><figcaption><p class="jm-lb-text" style="margin:0"></p>' +
				'<div class="jm-lb-btns">' + btn( 'jm-lb-prev', 'Previous image', 'M15 6l-6 6 6 6' ) +
				btn( 'jm-lb-next', 'Next image', 'M9 6l6 6-6 6' ) + btn( 'jm-lb-close', 'Close', 'M6 6l12 12M18 6L6 18' ) +
				'</div></figcaption></figure>';
			document.body.appendChild( box );
			document.body.classList.add( 'jm-modal-open' );
			show();
			box.addEventListener( 'click', function ( event ) {
				if ( event.target === box || event.target.closest( '.jm-lb-close' ) ) {
					close();
				} else if ( event.target.closest( '.jm-lb-prev' ) ) {
					index = ( index - 1 + list.length ) % list.length;
					show();
				} else if ( event.target.closest( '.jm-lb-next' ) ) {
					index = ( index + 1 ) % list.length;
					show();
				}
			} );
			box.querySelector( '.jm-lb-close' ).focus();
		}
		items.forEach( function ( it ) {
			var tile = it.querySelector( '.jm-g-img' );
			if ( ! tile ) {
				return;
			}
			tile.setAttribute( 'role', 'button' );
			tile.setAttribute( 'tabindex', '0' );
			tile.setAttribute( 'aria-label', 'View larger: ' + text( it, '.jm-g-title' ) );
			tile.addEventListener( 'click', function () {
				open( it );
			} );
			tile.addEventListener( 'keydown', function ( event ) {
				if ( 'Enter' === event.key || ' ' === event.key ) {
					event.preventDefault();
					open( it );
				}
			} );
		} );
		document.addEventListener( 'keydown', function ( event ) {
			if ( ! box ) {
				return;
			}
			if ( 'Escape' === event.key ) {
				close();
			} else if ( 'ArrowLeft' === event.key ) {
				index = ( index - 1 + list.length ) % list.length;
				show();
			} else if ( 'ArrowRight' === event.key ) {
				index = ( index + 1 ) % list.length;
				show();
			}
		} );
	}

	// Resources: topic chips show one group of resource cards at a time.
	function initResourceFilters() {
		var cards = document.querySelectorAll( '.jm-res-card' );
		var chips = document.querySelectorAll( '.jm-res-filters .jm-filter' );
		chips.forEach( function ( chip ) {
			chip.addEventListener( 'click', function () {
				var f = chip.getAttribute( 'data-filter' );
				chips.forEach( function ( c ) {
					c.setAttribute( 'aria-pressed', c === chip ? 'true' : 'false' );
				} );
				cards.forEach( function ( card ) {
					card.classList.toggle( 'is-hidden', 'all' !== f && ! card.classList.contains( 'jm-res-' + f ) );
				} );
			} );
		} );
	}

	// Card rows: give the titles in each visual row of a card grid the same height, so the text under
	// them starts on one line whatever wraps (buttons are pinned to the card foot in jm-site.css).
	function initCardAlign() {
		var grids = document.querySelectorAll( '.e-grid' );
		if ( ! grids.length ) {
			return;
		}
		function titleOf( card ) {
			var t = card.querySelector( '.jm-card-title, h2.elementor-heading-title, h3.elementor-heading-title' );
			return t ? t.closest( '.elementor-widget' ) : null;
		}
		function align() {
			grids.forEach( function ( grid ) {
				var rows = {};
				Array.prototype.forEach.call( grid.children, function ( card ) {
					var title = titleOf( card );
					if ( ! title ) {
						return;
					}
					title.style.minHeight = '';
					var top = Math.round( card.getBoundingClientRect().top + window.scrollY );
					( rows[ top ] = rows[ top ] || [] ).push( title );
				} );
				Object.keys( rows ).forEach( function ( top ) {
					var titles = rows[ top ];
					if ( titles.length < 2 ) {
						return;
					}
					var tallest = Math.max.apply( null, titles.map( function ( t ) {
						return t.getBoundingClientRect().height;
					} ) );
					titles.forEach( function ( t ) {
						t.style.minHeight = tallest + 'px';
					} );
				} );
			} );
		}
		var timer;
		function later() {
			clearTimeout( timer );
			timer = setTimeout( align, 120 );
		}
		align();
		window.addEventListener( 'resize', later );
		window.addEventListener( 'load', align );
		if ( document.fonts && document.fonts.ready ) {
			document.fonts.ready.then( align );
		}
	}

	function init() {
		document.querySelectorAll( '.jm-breath-toggle' ).forEach( initBreath );
		document.querySelectorAll( '.jm-hero video' ).forEach( initHeroVideo );
		initFootprints();
		initModals();
		initDesktopMenu();
		initGallery();
		initResourceFilters();
		initCardAlign();
	}

	if ( 'loading' === document.readyState ) {
		document.addEventListener( 'DOMContentLoaded', init );
	} else {
		init();
	}
	// Elementor injects the background video after its frontend boots.
	window.addEventListener( 'load', function () {
		document.querySelectorAll( '.jm-hero video' ).forEach( initHeroVideo );
	} );
}() );
