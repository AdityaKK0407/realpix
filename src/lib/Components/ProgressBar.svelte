<script lang="ts">
	import { range } from '$lib/scripts/utils';

	const numbers = range(1, 6);
</script>

<section>
	<div class="progress__container">
		<div class="progress__bar">
			<div class="progress"></div>
		</div>

		<ol class="progress__steps flex">
			{#each numbers as number (number)}
				<li class="progress__step">
					<span class="progress__number md-font-1">{number}</span>
				</li>
			{/each}
		</ol>
	</div>
</section>

<style>
	.progress__container {
		position: relative;
	}

	.progress__bar {
		width: 100%;
		height: 0.2rem;
		background-color: var(--color-bg-subtle);
		position: absolute;
		top: 50%;
		transform: translateY(-50%);
		z-index: -1;
	}

	.progress {
		width: 100%;
		height: 100%;
		background-color: var(--color-primary-900);
		transform: scaleX(0);
		transform-origin: 0;
		transition: transform 750ms cubic-bezier(0.86, 0, 0.14, 1);
	}

	.progress__steps {
		list-style-type: none;
		justify-content: center;
	}

	.progress__step {
		width: 3rem;
		height: 3rem;
		border-radius: 50vw;
		background-color: coral;
		display: flex;
		align-items: center;
		justify-content: center;
	}
</style>
