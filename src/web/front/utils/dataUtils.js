export function preprocessPatternsData(data) {
  const res = data.map((object) => {
    let date = new Date(object["date"]);
    date = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    return { ...object, date: date };
  });
  return res;
}
export function getColumn(arr, column) {
  return arr.map((object) => object[column]);
}

export function sum(arr) {
  return arr.reduce((sum, n) => sum + n, 0);
}

export function mean(arr) {
  return sum(arr) / arr.length;
}

export function uniqueValues(arr, property) {
  let uniqueValues = new Array();
  let currentAddedValues = new Set();
  arr.forEach((item) => {
    if (!currentAddedValues.has(item[property])) {
      uniqueValues.push(item);
      currentAddedValues.add(item[property]);
    }
  });
  return uniqueValues;
}
