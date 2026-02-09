function toTitleCase(stringVal: string) {
	const words = stringVal.split('');
	words[0] = words[0].toUpperCase();
	return words.join('');
}

export { toTitleCase };
