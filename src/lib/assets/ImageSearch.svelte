<script lang='ts'>
    interface Props {
        class?: string;
		size: number;
		ariaHidden?: boolean;
		ariaLabel?: string;
		strokeWidth?: number;
		fill?: string;
    }
    const props: Props = $props();
    const accessbilityLabels = $derived(
		props.ariaHidden
			? {
					'aria-hidden': true
				}
			: {
					role: 'img',
					'aria-label': props.ariaLabel,
					title: props.ariaLabel
				}
	);
</script>

<svg
    class={props.class}
	width={props.size}
	xmlns="http://www.w3.org/2000/svg"
	height={props.size}
	id="image-search"
	viewBox="-1087 2350 661 703"
	style="-webkit-print-color-adjust::exact"
	xmlns:xlink="http://www.w3.org/1999/xlink"
	fill={props.fill}
    stroke='currentColor'
    stroke-width={props.strokeWidth}
	version="1.1"
    {...accessbilityLabels}
>
	<g id="shape-35802bb9-e4b3-80d6-8007-c0549d1baa39" rx="0" ry="0">
		<g
			id="shape-35802bb9-e4b3-80d6-8007-c0509c81af91"
			fill='none'
			class="ionicon"
			rx="0"
			ry="0"
		>
			<g id="shape-35802bb9-e4b3-80d6-8007-c0509c84d777">
				<g class="fills" id="fills-35802bb9-e4b3-80d6-8007-c0509c84d777">
					<path
						d="M-1039,2478C-1039,2451.508056640625,-1017.491943359375,2430,-991,2430L-671,2430C-644.508056640625,2430,-623,2452.508056640625,-623,2479L-623,2734C-623,2760.491943359375,-644.508056640625,2782,-671,2782L-991,2782C-1017.491943359375,2782,-1039,2760.491943359375,-1039,2734L-1039,2478"
						fill={props.fill}
						stroke-linejoin="round"
						
					>
					</path>
				</g>
				<g
					fill={props.fill}
					stroke-linejoin="round"
					id="strokes-35802bb9-e4b3-80d6-8007-c05522f28764-35802bb9-e4b3-80d6-8007-c0509c84d777"
					class="strokes"
				>
					<g class="stroke-shape">
						<path
							d="M-1039,2478C-1039,2451.508056640625,-1017.491943359375,2430,-991,2430L-671,2430C-644.508056640625,2430,-623,2452.508056640625,-623,2479L-623,2734C-623,2760.491943359375,-644.508056640625,2782,-671,2782L-991,2782C-1017.491943359375,2782,-1039,2760.491943359375,-1039,2734L-1039,2478"
							fill={props.fill}   
                            stroke-width={props.strokeWidth}
						>
						</path>
					</g>
				</g>
			</g>
			<g id="shape-35802bb9-e4b3-80d6-8007-c0509c861e87">
				<g class="fills" id="fills-35802bb9-e4b3-80d6-8007-c0509c861e87">
					<path
						d="M-783,2685.7900390625L-873.6599731445312,2595.300048828125C-885.6357421875,2583.326904296875,-904.8662719726562,2582.757080078125,-917.5299682617188,2594L-1039,2702M-863,2782L-739.6599731445312,2658.659912109375C-727.96923828125,2646.94580078125,-709.2750854492188,2646.07861328125,-696.5499877929688,2656.659912109375L-623,2718"
						fill={props.fill}
						stroke-linecap="round"
						stroke-linejoin="round"
						
					>
					</path>
				</g>
				<g
					fill={props.fill}
					stroke-linecap="round"
					stroke-linejoin="round"
					id="strokes-35802bb9-e4b3-80d6-8007-c05522f5d544-35802bb9-e4b3-80d6-8007-c0509c861e87"
					class="strokes"
				>
					<g class="stroke-shape">
						<path
							d="M-783,2685.7900390625L-873.6599731445312,2595.300048828125C-885.6357421875,2583.326904296875,-904.8662719726562,2582.757080078125,-917.5299682617188,2594L-1039,2702M-863,2782L-739.6599731445312,2658.659912109375C-727.96923828125,2646.94580078125,-709.2750854492188,2646.07861328125,-696.5499877929688,2656.659912109375L-623,2718"
							fill={props.fill}   
                            stroke-width={props.strokeWidth}
						>
						</path>
					</g>
				</g>
			</g>
			<g id="shape-35802bb9-e4b3-80d6-8007-c0509c8592b8">
				<g class="fills" id="fills-35802bb9-e4b3-80d6-8007-c0509c8592b8">
					<ellipse
						cx="-876"
						cy="2498"
						rx="32"
						ry="32"
						transform="matrix(1.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000)"
						fill={props.fill}
						stroke-miterlimit="10"
					>
					</ellipse>
				</g>
				<g
					fill={props.fill}
					stroke-miterlimit="10"
					id="strokes-35802bb9-e4b3-80d6-8007-c05522f89501-35802bb9-e4b3-80d6-8007-c0509c8592b8"
					class="strokes"
				>
					<g class="stroke-shape">
						<ellipse
							cx="-876"
							cy="2498"
							rx="32"
							ry="32"
							transform="matrix(1.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000)"
                            fill={props.fill}   
                            stroke-width={props.strokeWidth}
						>
						</ellipse>
					</g>
				</g>
			</g>
			<g id="shape-35802bb9-e4b3-80d6-8007-c0509c835c33" style="display:none">
				<g class="fills" id="fills-35802bb9-e4b3-80d6-8007-c0509c835c33">
					<rect
						rx="0"
						ry="0"
						x="-1087"
						y="2350"
						transform="matrix(1.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000)"
						width="512.0000000000002"
						height="512"
						fill={props.fill}
						
					>
					</rect>
				</g>
			</g>
		</g>
		<g id="shape-35802bb9-e4b3-80d6-8007-c052b66a194d">
			<g class="fills" id="fills-35802bb9-e4b3-80d6-8007-c052b66a194d">
				<ellipse
					cx="-725.5"
					cy="2756"
					rx="196.5"
					ry="198.00000000000023"
					transform="matrix(1.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000)"
				>
				</ellipse>
			</g>
			<g
				id="strokes-35802bb9-e4b3-80d6-8007-c05522fb9494-35802bb9-e4b3-80d6-8007-c052b66a194d"
				class="strokes"
			>
				<g
					class="inner-stroke-shape"
					transform="matrix(1.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000)"
				>
					<defs>
						<clipPath id="inner-stroke-render-317-35802bb9-e4b3-80d6-8007-c052b66a194d-0">
							<use href="#stroke-shape-render-317-35802bb9-e4b3-80d6-8007-c052b66a194d-0"> </use>
						</clipPath>
						<ellipse
							cx="-725.5"
							cy="2756"
							rx="196.5"
							ry="198.00000000000023"
                            fill={props.fill}
                            stroke-width={props.strokeWidth}
							id="stroke-shape-render-317-35802bb9-e4b3-80d6-8007-c052b66a194d-0"
						>
						</ellipse>
					</defs>
					<use
						href="#stroke-shape-render-317-35802bb9-e4b3-80d6-8007-c052b66a194d-0"
						clip-path="url(&#x27;#inner-stroke-render-317-35802bb9-e4b3-80d6-8007-c052b66a194d-0&#x27;)"
					>
					</use>
				</g>
			</g>
		</g>
		<g
			id="shape-35802bb9-e4b3-80d6-8007-c0509c3789b6"
			style="fill:#000000"
			class="ionicon"
			rx="0"
			ry="0"
		>
			<g id="shape-35802bb9-e4b3-80d6-8007-c0509c3d3f8e" style="display:none">
				<g class="fills" id="fills-35802bb9-e4b3-80d6-8007-c0509c3d3f8e">
					<rect
						rx="0"
						ry="0"
						x="-952.9999999999986"
						y="2530"
						transform="matrix(1.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000)"
						width="527.0000000000001"
						height="523.0000000000014"
						fill={props.fill}
						
					>
					</rect>
				</g>
			</g>
			<g id="shape-35802bb9-e4b3-80d6-8007-c0509c3fe592">
				<g class="fills" id="fills-35802bb9-e4b3-80d6-8007-c0509c3fe592">
					<path
						d="M-725.432861328125,2595.375C-814.7327880859375,2595.37548828125,-887.1250610351562,2667.217529296875,-887.1250610351562,2755.83984375C-887.125,2844.46240234375,-814.7329711914062,2916.3046875,-725.4328002929688,2916.304931640625C-636.1327514648438,2916.305419921875,-563.740478515625,2844.46240234375,-563.7405395507812,2755.840087890625C-563.7461547851562,2667.22021484375,-636.1349487304688,2595.380859375,-725.432861328125,2595.375Z"
						fill={props.fill}
						stroke-miterlimit="10"
					>
					</path>
				</g>
				<g
					fill={props.fill}
					stroke-miterlimit="10"
					id="strokes-35802bb9-e4b3-80d6-8007-c05522ff2e9d-35802bb9-e4b3-80d6-8007-c0509c3fe592"
					class="strokes"
				>
					<g class="stroke-shape">
						<path
							d="M-725.432861328125,2595.375C-814.7327880859375,2595.37548828125,-887.1250610351562,2667.217529296875,-887.1250610351562,2755.83984375C-887.125,2844.46240234375,-814.7329711914062,2916.3046875,-725.4328002929688,2916.304931640625C-636.1327514648438,2916.305419921875,-563.740478515625,2844.46240234375,-563.7405395507812,2755.840087890625C-563.7461547851562,2667.22021484375,-636.1349487304688,2595.380859375,-725.432861328125,2595.375Z"
                            fill={props.fill}
                            stroke-width={props.strokeWidth}
						>
						</path>
					</g>
				</g>
			</g>
			<g id="shape-35802bb9-e4b3-80d6-8007-c0509c4175f5">
				<g class="fills" id="fills-35802bb9-e4b3-80d6-8007-c0509c4175f5">
					<path
						d="M-604.7991943359375,2875.55859375L-491.875,2987.624755859375"
						fill={props.fill}
						stroke-linecap="round"
						stroke-miterlimit="10"
						
					>
					</path>
				</g>
				<g
					fill={props.fill}
					stroke-linecap="round"
					stroke-miterlimit="10"
					id="strokes-35802bb9-e4b3-80d6-8007-c05523016a18-35802bb9-e4b3-80d6-8007-c0509c4175f5"
					class="strokes"
				>
					<g class="stroke-shape">
						<path
							d="M-604.7991943359375,2875.55859375L-491.875,2987.624755859375"
                            fill={props.fill}
                            stroke-width={props.strokeWidth}
						>
						</path>
					</g>
				</g>
			</g>
		</g>
		<g id="shape-35802bb9-e4b3-80d6-8007-c05411c35d2f">
			<g class="fills" id="fills-35802bb9-e4b3-80d6-8007-c05411c35d2f">
				<ellipse
					cx="-725.5"
					cy="2755"
					rx="150.5"
					ry="143.99999999999977"
					transform="matrix(1.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000)"
				>
				</ellipse>
			</g>
			<g
				id="strokes-35802bb9-e4b3-80d6-8007-c0552301ce19-35802bb9-e4b3-80d6-8007-c05411c35d2f"
				class="strokes"
			>
				<g
					class="inner-stroke-shape"
					transform="matrix(1.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000)"
				>
					<defs>
						<clipPath id="inner-stroke-render-322-35802bb9-e4b3-80d6-8007-c05411c35d2f-0">
							<use href="#stroke-shape-render-322-35802bb9-e4b3-80d6-8007-c05411c35d2f-0"> </use>
						</clipPath>
						<ellipse
							cx="-725.5"
							cy="2755"
							rx="150.5"
							ry="143.99999999999977"
							fill={props.fill}   
                            stroke-width={props.strokeWidth}
							id="stroke-shape-render-322-35802bb9-e4b3-80d6-8007-c05411c35d2f-0"
						>
						</ellipse>
					</defs>
					<use
						href="#stroke-shape-render-322-35802bb9-e4b3-80d6-8007-c05411c35d2f-0"
						clip-path="url(&#x27;#inner-stroke-render-322-35802bb9-e4b3-80d6-8007-c05411c35d2f-0&#x27;)"
					>
					</use>
				</g>
			</g>
		</g>
	</g>
</svg>