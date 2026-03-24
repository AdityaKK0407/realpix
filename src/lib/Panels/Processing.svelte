<script lang="ts">
	import { processingStatus } from '$lib/state/processingResult.svelte';
	import { type FileType, uploadData } from '$lib/state/uploadFlow.svelte';

	interface Props {
		fileType: FileType;
	}

	const props: Props = $props();

	async function upload() {
		const packages = uploadData.createPackages(props.fileType);
		console.log(packages);
		if (packages) {
			try {
				const package1Response = await fetch('/api/uploadImage', {
					method: 'POST',
					body: packages.package1
				});
				let package2Response = null;

				if (package1Response.ok) {
					const package1Data = await package1Response.json();
					processingStatus.addTasks(package1Data.data.task_ids);
					if (packages.package2) {
						package2Response = await fetch('/api/uploadImage', {
							method: 'POST',
							body: packages.package2
						});
						if (!package2Response.ok) {
							alert('error');
							return;
						} else if (packages.moreBatchAvailable) {
							alert('More packages available');
						}

						const package2Data = await package2Response.json();
						processingStatus.addTasks(package2Data.data.task_ids);

						processingStatus.startPinging();
					}
				} else {
					alert(package1Response.statusText);
					return;
				}
			} catch (err) {
				alert(`Error occured: ${err}`);
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
