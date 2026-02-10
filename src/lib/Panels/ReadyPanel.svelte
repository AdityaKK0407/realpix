<script lang="ts">
	import {
		getNamesOfType,
		returnBlobs,
		returnFileType,
		returnLength,
		returnLengthOne
	} from '$lib/state/uploadFlow.store';
	import { onDestroy } from 'svelte';
	import { range } from '$lib/scripts/utils';
	import { ImagePlus } from 'lucide-svelte';

	interface Props {
		fileType: 'image' | 'video';
	}

	const index = $state(0);
	const props: Props = $props();
	const fileType = returnFileType(props.fileType);
	const urls = returnBlobs(props.fileType);
	const names = getNamesOfType(props.fileType);
	const selectedImage = $derived(urls[index]);
	const selectedName = $derived(names[index]);
	const oneImage = returnLengthOne(props.fileType);
	const length = returnLength(props.fileType);
	const remainingLength = range(length + 1, 5);

	onDestroy(() => {
		urls.forEach((url) => URL.revokeObjectURL(url));
	});
</script>

<section class="ready-container" class:bigImage={oneImage} class:smallImage={!oneImage}>
	<section class="image-container">
		<img src={selectedImage} alt={`Image:- ${selectedName}`} aria-hidden="true" class:max={oneImage}
				 class:small={!oneImage} />
	</section>
	<section class:oneLayout={oneImage}>
		{#if oneImage}
			<p class="md-font-2 bold">Image 1 ({selectedName})</p>
		{:else if !oneImage}
			<section class="flex-column">
				<section>
					<p class="sm-font-3 bold">{index + 1} / {length} images filled</p>
				</section>
				<section class="buttons">
					{#each fileType as image (image.id)}
						<button class="sm-font-4 iconImage">
							<img src={image.blob} alt={`Image:- ${image.name}`} />
							{image.name}
						</button>
					{/each}
					{#each remainingLength as no (no)}
						<button>
							<ImagePlus />
						</button>
					{/each}
				</section>
			</section>
		{/if}
	</section>
</section>

<style>
    .ready-container {
        flex-grow: 1;
        display: grid;
    }

    .bigImage {
        grid-template-rows: 0.7fr 0.15fr 0.15fr;
    }

    .smallImage {
        grid-template-rows: 0.55fr 0.34fr 0.11fr;
    }

    .image-container {
        background-color: var(--color-primary-lowest);
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 2rem;
        padding: var(--small-padding);
    }

    .oneLayout {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .buttons {
        display: flex;
        gap: var(--text-gap);
        justify-content: center;
        align-items: center;
    }

    .iconImage {
        width: 17%;
        letter-spacing: 0.01em;
        line-height: 1.3;
        padding: var(--small-padding);
        border-radius: 1rem;
        background-color: transparent;
    }

    img {
        max-width: 100%;
        max-height: 100%;
        height: auto;
        object-fit: contain;
        display: block;
    }

    img.small {
        width: 55%;
    }

    img.max {
        width: 60%;
    }
</style>
