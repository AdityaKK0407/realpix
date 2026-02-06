<script lang="ts">

	import { Check, CircleAlert } from 'lucide-svelte';
	import { validateFiles } from '$lib/scripts/validatingFiles';
	import type { FileUploadOptions } from '$lib/types/fileupload.types';


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
</script>

<section class="flex-column uploadSection">
	<h2 class="lg-font-1">
		{headerText}
	</h2>
	<div
		role="button"
		tabindex={uploadState === 'successState' ? -1 : 0}
		class='dropzone'
		class:error={uploadState === 'errorState'}
		class:dropping={uploadState === 'draggingState'}
		class:neutral={uploadState === 'resetState'}
		class:success={uploadState === 'successState'}
		ondragover={(e) => setState(e, 'draggingState')}
		ondragleave={(e) => setState(e, 'resetState')}
		ondrop={drop}
		onkeydown={keyBoardEvent}
		onclick={() => {
			if(uploadState === 'resetState' || uploadState === 'errorState') {
				fileInput.click()
			}}}
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
				<span class="material-symbols-outlined uploadIcon muted">
					image_inset
				</span>
				<section class="dropzone-secondary-text flex-column">
					<strong class="lg-font-2 primary">Drop images here</strong>
					<p class="md-font-1 bodycolor">or click to browse</p>
				</section>

			</section>

		{:else if uploadState === 'successState' }
			<section class="flex-column successText">
				<p class="sr-only" aria-live="polite">{screenReaderMessage}</p>
				<Check size="40" aria-hidden="true" />
				<p class="md-font-2 bold" aria-hidden="true">{successText}</p>
			</section>

		{:else if uploadState === 'draggingState' }
			<section class="drop-field flex-column">
				<span class="material-symbols-outlined uploadIcon">
					image_inset
				</span>
				<p class="md-font-1 bold">Drop the file</p>
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
	<small class="sm-font-1 muted">{props.extensions}</small>
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
        height: 15rem;
        border-width: 0.25rem;
        width: 100%;
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
        font-size: 3.2rem;
    }
</style>