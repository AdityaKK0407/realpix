<script lang="ts">
	import { browser } from '$app/environment';
	import { uploadData, type FileType } from '$lib/state/uploadFlow.store';
	import { ImagePlus } from 'lucide-svelte';
	import { onMount } from 'svelte';

	interface Props {
		fileType: FileType;
	}

	const props: Props = $props();
	let index: string = $state('');

	onMount(() => {
		index = uploadData.getFileTypeFirstId(props.fileType)
	})

	const fileType = uploadData.getFileType(props.fileType);
	let selectedImage = $derived(browser && index ? uploadData.getFileBlob(index) : '')
	const selectedName = $derived(browser && index ? uploadData.getName(index) : "");
	const length = uploadData.getLength(props.fileType);
	const oneImage = length === 1;
	const remainingLength = uploadData.getMaxLength();

	function changeIndex(num: string) {
		index = num;
	}
</script>

<section class="ready-container" class:bigImage={oneImage} class:smallImage={!oneImage}>
	<section class="image-container">
		<img
			src={selectedImage}
			alt={`Image:- ${selectedName}`}
			aria-hidden="true"
			class:max={oneImage}
			class:small={!oneImage}
		/>
	</section>
	<section class:oneLayout={oneImage}>
		{#if oneImage}
			<p class="md-font-2 bold">Image 1 ({selectedName})</p>
		{:else if !oneImage}
			<section class="flex-column">
				<section>
					<p class="sm-font-3 bold">{length} / {remainingLength} images filled</p>
				</section>
				<section class="buttons">
					{#each fileType as image (image.id)}
						<button class="sm-font-4 iconImage transparent" onclick={() => changeIndex(image.id)}>
							<img src={image.blob} alt={`Image:- ${image.name}`} class="buttonImg"/>
							{image.name}0
						</button>
					{/each}
					{#if length !== remainingLength}
						<button class="sm-font-2 addButton background-color-pri-lowest color-pri">
							<ImagePlus color="currentColor" />
						</button>
					{/if}
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
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
		gap: var(--text-gap);
		justify-content: center;
	}

	.iconImage {
		width: clamp(1.5rem, 13vw, 18rem);
		height: clamp(1.6rem, 8.7vw, 12rem);
		letter-spacing: 0.01em;
		line-height: 1.3;
		border-radius: 1rem;
	}

	.addButton {
		padding: var(--medium2-padding);
		border: 0.16rem var(--color-primary-300) dotted;
		display: flex;
		justify-content: center;
		align-items: center;
		border-radius: 1.2rem;
	}

	.buttonImg {
		display: block;
		object-fit: cover;
		height: clamp(1.4rem, 7vw, 8rem);
	}

	img {
		max-width: 100%;
		height: auto;
		object-fit: cover;
		display: block;
	}

	img.small {
		max-height: 20rem;
	}

	img.max {
		max-height: 23rem;
	}
</style>
