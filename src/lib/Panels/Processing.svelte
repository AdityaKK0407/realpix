<script lang="ts">
	import { type FileType, uploadData } from '$lib/state/uploadFlow.svelte';

	interface Props {
		fileType: FileType;
	}

	const props: Props = $props();
	const data = $derived(uploadData.getFileType(props.fileType));

	async function upload() {
		if (data) {
			const packages = uploadData.createPackages(props.fileType);

			try {
				const package1Response = await fetch('/api/uploadImage', {
					method: 'POST',
					body: packages.package1
				});

				if (package1Response.ok) {
					if (packages.package2) {
						const package2Response = await fetch('/api/uploadImage', {
							method: 'POST',
							body: packages.package2
						});
						if (!package2Response.ok) {
							alert('error');
						} else if (packages.moreBatchAvailable) {
							alert('More packages available');
						}
					}
				} else {
					alert('error');
				}
			} catch (err) {
				alert(`Error occured: ${err}`);
				console.log(err);
			}
		}
	}

	upload();
</script>

<section class="uploading__container">
	<p>Uploaded</p>
</section>

<style>
	.uploading__container {
		flex-grow: 1;
	}
</style>
