<?php
/**
 * Jennifer Malecki (Hello Elementor Child) functions.
 *
 * The parent theme enqueues its own stylesheets. This child adds the site
 * design layer: every stylesheet in assets/css and every script in
 * assets/js, loaded in file-name order after Elementor's frontend CSS.
 */

defined( 'ABSPATH' ) || exit;

add_action( 'wp_enqueue_scripts', function () {
	$dir = get_stylesheet_directory();
	$uri = get_stylesheet_directory_uri();

	$deps = array( 'hello-elementor' );
	if ( wp_style_is( 'elementor-frontend', 'registered' ) ) {
		$deps[] = 'elementor-frontend';
	}

	foreach ( (array) glob( $dir . '/assets/css/*.css' ) as $file ) {
		$name = basename( $file, '.css' );
		wp_enqueue_style( 'jm-' . $name, $uri . '/assets/css/' . basename( $file ), $deps, (string) filemtime( $file ) );
		$deps = array( 'jm-' . $name );
	}

	foreach ( (array) glob( $dir . '/assets/js/*.js' ) as $file ) {
		$name = basename( $file, '.js' );
		wp_enqueue_script( 'jm-' . $name, $uri . '/assets/js/' . basename( $file ), array(), (string) filemtime( $file ), array( 'in_footer' => true, 'strategy' => 'defer' ) );
	}
}, 20 );

/**
 * Let administrators upload SVG files so line icons can be picked in
 * Elementor's Icon widget (Upload SVG). Elementor sanitises inline SVGs
 * when it renders them.
 */
add_filter( 'upload_mimes', function ( $mimes ) {
	if ( current_user_can( 'manage_options' ) ) {
		$mimes['svg'] = 'image/svg+xml';
	}
	return $mimes;
} );

add_filter( 'wp_check_filetype_and_ext', function ( $data, $file, $filename ) {
	if ( current_user_can( 'manage_options' ) && 'svg' === strtolower( pathinfo( $filename, PATHINFO_EXTENSION ) ) ) {
		$data['ext']  = 'svg';
		$data['type'] = 'image/svg+xml';
	}
	return $data;
}, 10, 3 );
