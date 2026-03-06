<script lang="ts">
	import { uploadData, type FileType } from '$lib/state/uploadFlow.store';
	import { transition } from '$lib/upload/upload.store';
	import { CircleX, ImagePlus, ScanSearch } from 'lucide-svelte';
	import { onMount } from 'svelte';

	interface Props {
		fileType: FileType;
	}

	const props: Props = $props();
	let index: string = $state('');

	onMount(() => {
		index = uploadData.getFileTypeFirstId(props.fileType)!;
	});

	const fileType = uploadData.getFileType(props.fileType);
	let selectedImage = $derived(uploadData.getFileBlob(index));
	const selectedName = $derived(uploadData.getName(index));
	const length = uploadData.getLength(props.fileType);
	const oneImage = length === 1;
	const remainingLength = uploadData.getMaxLength();

	function changeIndex(num: string) {
		index = num;
	}

	function handleAnaylzeClick(): void {
		transition('START_UPLOAD');
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
			loading="lazy"
		/>
	</section>
	<section class:oneLayout={oneImage}>
		{#if oneImage}
			<p class="md-font-2 bold">Image 1 ({selectedName})</p>
		{:else if !oneImage}
			<section class="flex-column imageDisplay">
				<section>
					<p class="sm-font-3 bold">{length} / {remainingLength} images filled</p>
				</section>
				<section class="buttons">
					{#each fileType as image (image.id)}
						<button
							class="sm-font-4 iconImage transparent flex-column bold"
							class:selected={image.id === index}
							onclick={() => changeIndex(image.id)}
						>
							<img src={image.blob} alt={`Image:- ${image.name}`} class="buttonImg" />
							{image.name}
						</button>
					{/each}
					{#if length !== remainingLength}
						<section class="addButton__container">
							<button class="sm-font-2 addButton background-color-pri-lowest color-pri">
								<ImagePlus color="currentColor" />
								<p class="sr-only">To add more files, click this button</p>
							</button>
						</section>
					{/if}
				</section>
			</section>
		{/if}
	</section>
	<section class="btn-container">
		<button class="btn primary-btn md-font-1 medium-bold" onclick={handleAnaylzeClick}>
			<ScanSearch stroke-width={2} />
			Analyze
		</button>
		<button class="btn secondary-btn md-font-1">
			<CircleX />
			Cancel
		</button>
	</section>
</section>

<style>
	.ready-container {
		flex-grow: 1;
		display: grid;
		gap: var(--text-gap);
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

	.imageDisplay {
		gap: 0.5rem;
	}

	.iconImage {
		gap: var(--text-gap);
		align-items: center;
		letter-spacing: 0.01em;
		line-height: 1.3;
		border-radius: 1rem;
		padding: var(--small-padding);
		outline: transparent 0.15rem solid;
		transition: outline-color 450ms ease-in-out;
	}

	.iconImage.selected {
		outline-color: var(--color-primary-800);
	}

	.addButton__container {
		display: flex;
		justify-content: center;
		align-items: center;
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
		height: clamp(1.3rem, 5.5vw, 7rem);
	}

	img {
		max-width: 100%;
		object-fit: cover;
		display: block;
	}

	img.small {
		height: 18rem;
	}

	img.max {
		height: 20rem;
	}

	.btn-container {
		display: flex;
		flex-direction: row-reverse;
		gap: var(--text-gap-large);
		align-items: center;
	}
</style>
