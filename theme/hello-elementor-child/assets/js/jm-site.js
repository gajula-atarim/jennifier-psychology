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

	function init() {
		document.querySelectorAll( '.jm-breath-toggle' ).forEach( initBreath );
		document.querySelectorAll( '.jm-hero video' ).forEach( initHeroVideo );
		initFootprints();
		initModals();
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
