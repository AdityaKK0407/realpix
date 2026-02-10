function range(start: number, end: number) {
	const array = [];
	for (let i = start; i < end; i++) {
		array.push(i);
	}
	return array;
}

function toTitleCase(stringVal: string) {
	const words = stringVal.split('');
	words[0] = words[0].toUpperCase();
	return words.join('');
}

function addSBasedOnCondition(condition: boolean, value: string) {
		return condition ? `${value}s` : value
}

export { range, toTitleCase, addSBasedOnCondition };
