<script lang="ts">
	import { CircleAlert, CircleCheckBigIcon, Info } from 'lucide-svelte';
	import { validateFiles } from '$lib/scripts/validatingFiles';
	import type { FileUploadOptions } from '$lib/types/fileupload.types';
	import UploadingMetrics from './UploadingMetrics.svelte';
	import { addSBasedOnCondition, range, toTitleCase } from '$lib/scripts/utils';

	interface Props {
		onSelect: (newFiles: File[], fileType: 'image' | 'video') => void;
		fileType: 'image' | 'video';
		extensions: 'PNG, JPG, JPEG' | 'Video';
	}

	let props: Props = $props();

	let fileInput: HTMLInputElement;
	let uploadState: FileUploadOptions = $state('resetState');
	let successText: string = $state('');
	let screenReaderMessage: string = $state('');
	let headerText: string = $state(`Upload ${props.fileType}`);
	const numbers = range(1, 8);

	function handleFiles(files: FileList) {
		if (files.length > 0) {
			if (props.fileType == 'image') {
				const filesArray = Array.from(files);
				const filteredFilesArray = validateFiles(filesArray);
				if (filteredFilesArray.length > 0) {
					uploadState = 'successState';
					successText = `${addSBasedOnCondition(filteredFilesArray.length > 1, 'File')} uploaded successfully.`;
					screenReaderMessage = `${files.length === 1 ? 'One' : files.length} files have been selected successfully.`;
					props.onSelect(Array.from(filteredFilesArray), props.fileType);
					headerText = `Uploaded ${addSBasedOnCondition(filteredFilesArray.length > 1, 'File')}`;
				} else {
					uploadState = 'errorState';
				}
			}
		}
	}

	function setState(e: DragEvent, value: FileUploadOptions) {
		e.preventDefault();
		uploadState = value;
	}

	function keyBoardEvent(e: KeyboardEvent) {
		if (e.key === 'Enter' || e.key === ' ') {
			fileInput.click();
		}
	}

	function inputChange(e: Event) {
		e.preventDefault();
		const target = e.target as HTMLInputElement;
		if (target.files) {
			handleFiles(target.files);
		}
	}

	function drop(e: DragEvent) {
		if (e.dataTransfer) {
			e.preventDefault();
			handleFiles(e.dataTransfer.files);
		}
	}

	function handleClick(e: Event) {
		e.preventDefault();
		if (uploadState === 'resetState' || uploadState === 'errorState') {
			fileInput.click();
		}
	}
</script>

<section class="flex-column uploadSection">
	<h2 class="lg-font-1">
		{headerText}
	</h2>
	<div
		role="button"
		tabindex={uploadState === 'successState' ? -1 : 0}
		class="dropzone"
		class:error={uploadState === 'errorState'}
		class:dropping={uploadState === 'draggingState'}
		class:background_color_pri_lowest={uploadState === 'draggingState'}
		class:neutral={uploadState === 'resetState'}
		class:success={uploadState === 'successState'}
		ondragover={(e) => setState(e, 'draggingState')}
		ondragleave={(e) => setState(e, 'resetState')}
		ondrop={drop}
		onkeydown={keyBoardEvent}
		aria-label="Drag and drop images area"
	>
		<input
			type="file"
			class="hidden"
			bind:this={fileInput}
			onchange={inputChange}
			accept="image/*"
			multiple
		/>

		{#if uploadState === 'resetState'}
			<section class="dropzone-text flex-column">
				<div class="iconField background-color-pri-100 color-pri">
					<span class="material-symbols-outlined uploadIcon"> image_inset </span>
				</div>
				<section class="dropzone-secondary-text flex-column">
					<strong class="lg-font-2 primary-text">Drop {props.fileType}s here</strong>
					<p class="sm-font-2 bodycolor">Max file limit: 5</p>
					<small class="sm-font-1 muted">{props.extensions}</small>
				</section>
				<button
					onclick={handleClick}
					class="click-button bold sm-font-1"
					aria-label={`This button opens the file explorer to select the ${props.fileType}s`}
				>
					Select {props.fileType}s
				</button>
			</section>
		{:else if uploadState === 'successState'}
			<section class="flex-column successText">
				<p class="sr-only" aria-live="polite">{screenReaderMessage}</p>
				<section class="successIcon" aria-hidden="true">
					<CircleCheckBigIcon size="40" />
				</section>
				<p class="md-font-2 bold align-center" aria-hidden="true">{successText}</p>
			</section>
		{:else if uploadState === 'draggingState'}
			<section class="drop-field flex-column">
				<div class="iconField background-color-pri-900 color-text-pri pulse">
					<span class="material-symbols-outlined uploadIcon"> image_inset </span>
					{#each numbers as number (number)}
						<span style={`--i: ${number}`} class="animate-element"></span>
					{/each}
				</div>
				<section class="flex-column dropzone-secondary-text">
					<p class="md-font-2 bold">Drop the {props.fileType}</p>
					<p class="sm-font-2 bold">Max file limit: 5</p>
				</section>
			</section>
		{:else if uploadState === 'errorState'}
			<section class="dropzone-text flex-column errorSection">
				<CircleAlert size="48" />
				<section class="dropzone-secondary-text flex-column">
					<strong class="lg-font-2">Upload failed</strong>
					<p class="md-font-1">Please select a valid {props.fileType} file</p>
				</section>
			</section>
		{/if}
	</div>
	<UploadingMetrics />
	<section class="footer-content">
		<Info size="24" stroke="currentColor" />
		<p class="sm-font-3">
			<strong>Note: </strong>
			{toTitleCase(props.fileType)}(s) are deleted after processing
		</p>
	</section>
</section>

<style>
	section {
		width: 100%;
	}

	.uploadSection {
		gap: var(--text-gap-large);
		align-items: center;
		justify-content: space-evenly;
	}

	.dropzone {
		display: flex;
		flex-direction: column;
		gap: 0.9rem;
		justify-content: center;
		align-items: center;
		padding-inline: var(--file-upload-padding-inline);
		padding-block: var(--file-upload-padding-block);
		border-radius: 0.6rem;
		border-width: 0.25rem;
		width: 100%;
		height: 18rem;
	}

	.dropzone-text {
		gap: 1rem;
		align-items: center;
	}

	.dropzone-secondary-text {
		gap: 0.27rem;
		align-items: center;
	}

	.neutral {
		border-style: dashed;
		border-color: var(--color-border-neutral);
	}

	.dropping {
		border-color: var(--color-border-dragover);
		border-style: solid;
		color: var(--color-primary);
	}

	.dropping > * {
		pointer-events: none;
	}

	.drop-field {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: var(--text-gap-large);
	}

	.success {
		border-color: var(--color-border-success);
		background-color: var(--color-success-lowest);
		color: var(--color-text-success);
		pointer-events: none;
		border-width: 0.19rem;
		border-style: dotted;
	}

	.successText {
		gap: var(--text-gap);
		align-items: center;
		justify-content: center;
	}

	.successIcon {
		width: max-content;
		background-color: var(--color-success-100);
		display: flex;
		justify-content: center;
		border-radius: 50vw;
		padding: var(--small-padding);
	}

	.error {
		background-color: var(--color-bg-error);
		border-color: var(--color-border-error);
		border-style: dotted;
	}

	.errorSection {
		color: var(--color-text-error);
	}

	.uploadIcon {
		font-size: 3rem;
	}

	.pulse {
		display: grid;
		border: 1px solid var(--color-primary-500);
		box-shadow:
			inset 0 0 2.5rem var(--color-primary-500),
			0 0 3.125rem var(--color-primary-500);
	}

	.pulse > * {
		grid-row-start: 1;
		grid-column-start: 1;
	}

	.pulse > .animate-element {
		width: 100%;
		height: 100%;
		background-color: transparent;
		border: 1px solid var(--color-primary-400);
		border-radius: 50vw;
		animation: animate 6s linear infinite;
		animation-delay: calc(var(--i) * -1.2s);
	}

	@keyframes animate {
		0% {
			scale: 1;
			opacity: 1;
		}
		50% {
			opacity: 0.6;
		}
		75% {
			opacity: 0.2;
		}
		100% {
			scale: 3;
			opacity: 0;
		}
	}

	.click-button {
		background-color: var(--color-primary);
		color: var(--color-primary-text);
		padding-inline: var(--primary-button-padding-inline);
		padding-block: var(--primary-button-padding-inline);
		border-radius: 1.4rem;
		filter: drop-shadow(0 0.125rem 0.55rem var(--color-primary-400));
		transition:
			background-color 400ms ease-in-out,
			filter 385ms ease-in-out;
	}

	.click-button:hover {
		background-color: var(--color-primary-hover);
		filter: drop-shadow(0px 0.25rem 0.6rem var(--color-primary-600));
	}

	.footer-content {
		display: flex;
		gap: var(--text-gap);
		justify-content: center;
		align-items: center;
		color: var(--color-primary-900);
	}
</style>
