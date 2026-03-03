<script lang="ts">
	import type { Colors } from '$lib/types/fileupload.types';

	interface Props {
		color: Colors;
	}
	const props: Props = $props();
</script>

<svg
	xmlns="http://www.w3.org/2000/svg"
	width="56"
	height="56"
	viewBox="0 0 58 58"
	fill="none"
	class:shieldIcon={true}
	class:red={props.color === 'red'}
	class:yellow={props.color === 'yellow'}
	class:periwinkle={props.color === 'periwinkle'}
	class:gray={props.color === 'gray'}
	class:security-green={props.color === 'security-green'}
	aria-hidden="true"
>
	<path
		d="M42.3034 28.913C42.3034 38.4776 35.6082 43.2599 27.6504 46.0336C27.2337 46.1748 26.7811 46.1681 26.3688 46.0145C18.3919 43.2599 11.6967 38.4776 11.6967 28.913V15.5225C11.6967 15.0152 11.8982 14.5286 12.2569 14.1699C12.6157 13.8112 13.1022 13.6096 13.6096 13.6096C17.4354 13.6096 22.2177 11.3141 25.5462 8.40647C25.9515 8.06023 26.467 7.87 27 7.87C27.5331 7.87 28.0486 8.06023 28.4538 8.40647C31.8015 11.3332 36.5646 13.6096 40.3905 13.6096C40.8978 13.6096 41.3844 13.8112 41.7431 14.1699C42.1019 14.5286 42.3034 15.0152 42.3034 15.5225V28.913Z"
		stroke="currentColor"
		fill="currentColor"
		stroke-linecap="round"
		stroke-linejoin="round"
		stroke-width="1.5"
		class="layer-0"
		data-layer="layer-0"
	/>
	<path
		d="M26.9999 41.684C34.8087 41.684 41.1389 35.3537 41.1389 27.545C41.1389 19.7362 34.8087 13.406 26.9999 13.406C19.1912 13.406 12.861 19.7362 12.861 27.545C12.861 35.3537 19.1912 41.684 26.9999 41.684Z"
		stroke="currentColor"
		fill="currentColor"
		stroke-linecap="round"
		stroke-linejoin="round"
		class="layer-1"
		data-layer="layer-1"
	/>
	<path
		d="M27 49.5C39.4264 49.5 49.5 39.4264 49.5 27C49.5 14.5736 39.4264 4.5 27 4.5C14.5736 4.5 4.5 14.5736 4.5 27C4.5 39.4264 14.5736 49.5 27 49.5Z"
		stroke="currentColor"
		fill="currentColor"
		stroke-linecap="round"
		stroke-linejoin="round"
		class="layer-2"
		data-layer="layer-2"
	/>
</svg>

<style>
	/* Animation Styles */
	.shieldIcon {
		--layer-1-time: 15s;
		--layers-time: 10s;
		transition: color 250ms ease-in-out;
	}

	.yellow {
		color: var(--color-yellow);
	}

	.periwinkle {
		color: var(--color-primary);
	}

	.red {
		color: var(--color-error);
	}

	.gray {
		color: var(--color-text-muted);
	}

	.security-green {
		color: var(--color-success-green);
	}

	.layer-0 {
		animation: layer-0 cubic-bezier(0.66, 0.04, 0.38, 0.9) var(--layer-1-time) infinite;

		transform-box: fill-box;
	}

	.layer-1 {
		animation: layer-1 linear var(--layers-time) infinite;

		transform-box: fill-box;
	}

	.layer-2 {
		animation: layer-2 ease-in-out var(--layers-time) infinite;

		transform-box: fill-box;
	}

	@keyframes layer-0 {
		0% {
			opacity: 1;
			transform-origin: center center;
			transform: scale(0.98);
		}
		50% {
			opacity: 0.98;
			transform-origin: center center;
			transform: scale(1.05);
		}
		100% {
			opacity: 1;
			transform-origin: center center;
			transform: scale(0.98);
		}
	}

	@keyframes layer-1 {
		0% {
			opacity: 0.18;
			transform-origin: center center;
			transform: scale(1);
		}
		50% {
			opacity: 0.25;
			transform-origin: center center;
			transform: scale(1.75);
		}
		100% {
			opacity: 0.18;
			transform-origin: center center;
			transform: scale(1);
		}
	}

	@keyframes layer-2 {
		0% {
			opacity: 0.12;
			transform-origin: center center;
			transform: scale(1);
		}
		50% {
			opacity: 0.15;
			transform-origin: center center;
			transform: scale(1.4);
		}
		100% {
			opacity: 0.12;
			transform-origin: center center;
			transform: scale(1);
		}
	}
</style>
