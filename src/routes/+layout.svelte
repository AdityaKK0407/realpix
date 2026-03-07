<script lang="ts">
	import '$lib/css/variables.css';
	import '$lib/css/styles.css';
	import '$lib/css/utilities.css';
</script>

<svelte:head>
	<meta
		name="description"
		content="Detect deepfakes and verify image authenticity with RealPix's AI powered tool. Upload upto 5 images and get fast analysis. Secure, encrypted and easy to use."
	/>

	<meta
		name="keywords"
		content="deepfake detection, AI detection tool, fake image detector, image verification, photo authenticity checker, AI image analysis, free deepfake detector"
	/>

	<meta property="org:type" content="website" />
	<meta property="og:url" content="https://fab-realpix.netlify.app" />
	<meta property="og:title" content="RealPix - AI Deepfake Detection Tool" />
	<meta
		property="og:description"
		content="Detect deepfakes and verify the authenticity of images instantly with AI powered analysis to identify manipulated images."
	/>

	<meta property="twitter:card" content="summary_large_image" />
	<meta property="twitter:url" content="https://fab-realpix.netlify.app" />
	<meta property="twitter:title" content="RealPix - AI Deepfake Detection Tool" />
	<meta
		property="twitter:description"
		content="Detect deepfakes and verify the authenticity of images instantly with AI powered analysis to identify manipulated images."
	/>

	{@html `<script type='application/ld+json'>
		"@context": "https://schema.org/",
		"@type": "SoftwareApplication",
		"name": "RealPix",
		"applicationCategory": "SecurityApplication",
		"operatingSystem": "Web Browser",
		"offers": {
			"@type": "Offer,",
			"price": "0",
			"priceCurrency": "USD"
		},
		"description": "AI-powered deepfake detection and image authenticity verification tool",
	<\/script>`}

	<link rel="canonical" href="https://fab-realpix.netlify.app" />
</svelte:head>

<slot />
