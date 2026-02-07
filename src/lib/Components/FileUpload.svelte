<script lang="ts">
	import { Check, CircleAlert, Sparkles } from 'lucide-svelte';
	import { validateFiles } from '$lib/scripts/validatingFiles';
	import type { FileUploadOptions } from '$lib/types/fileupload.types';
	import UploadingMetrics from './UploadingMetrics.svelte';

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

	function getFileOrFiles(files: File[]) {
		return files.length > 1 ? 'Files' : 'File';
	}

	function handleFiles(files: FileList) {
		if (files.length > 0) {
			if (props.fileType == 'image') {
				const filesArray = Array.from(files);
				const filteredFilesArray = validateFiles(filesArray);
				if (filteredFilesArray.length > 0) {
					uploadState = 'successState';
					successText = `${getFileOrFiles(filteredFilesArray)} uploaded successfully.`;
					screenReaderMessage = `${files.length === 1 ? 'One' : files.length} files have been selected successfully.`;
					props.onSelect(Array.from(filteredFilesArray), props.fileType);
					headerText = `Uploaded ${getFileOrFiles(filteredFilesArray)}`;
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
				<div class="iconField neutralIconField">
					<span class="material-symbols-outlined uploadIcon"> image_inset </span>
				</div>
				<section class="dropzone-secondary-text flex-column">
					<strong class="lg-font-2 primary">Drop {props.fileType}s here</strong>
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
				<Check size="40" aria-hidden="true" />
				<p class="md-font-2 bold" aria-hidden="true">{successText}</p>
			</section>
		{:else if uploadState === 'draggingState'}
			<section class="drop-field flex-column">
				<div class="iconField draggingIconField">
					<span class="material-symbols-outlined uploadIcon"> image_inset </span>
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
</section>

<style>
	section {
		width: 100%;
	}

	.uploadSection {
		gap: 1rem;
		align-items: center;
		justify-content: space-evenly;
		height: 100%;
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
		cursor: pointer;
	}

	.dropping {
		background-color: var(--color-bg-dragover);
		border-color: var(--color-border-dragover);
		border-style: solid;
		cursor: default;
		color: var(--color-text-dragover);
	}

	.dropping > * {
		pointer-events: none;
	}

	.drop-field {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: var(--text-gap);
	}

	.success {
		border-color: var(--color-border-success);
		background-color: var(--color-bg-success);
		color: var(--color-text-success);
		pointer-events: none;
		border-style: dotted;
	}

	.successText {
		align-items: center;
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

	.neutralIconField {
		background-color: rgba(0 0 0 / 0.08);
	}

	.draggingIconField {
		background-color: #fafafa;
	}

	.click-button {
		background-color: var(--color-primary);
		color: var(--color-primary-text);
		padding-inline: var(--primary-button-padding-inline);
		padding-block: var(--primary-button-padding-inline);
		border-radius: 1.4rem;
		filter: drop-shadow(0 0.125rem 0.5rem rgba(82 105 143 / 0.3));
		transition:
			background-color 400ms ease-in-out,
			filter 385ms ease-in-out;
	}

	.click-button:hover {
		background-color: var(--color-primary-hover);
		filter: drop-shadow(0px 0.25rem 0.75rem rgba(82 105 143 / 0.35));
	}
</style>
