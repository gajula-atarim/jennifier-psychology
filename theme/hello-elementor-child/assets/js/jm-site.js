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

	function init() {
		document.querySelectorAll( '.jm-breath-toggle' ).forEach( initBreath );
		document.querySelectorAll( '.jm-hero video' ).forEach( initHeroVideo );
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
