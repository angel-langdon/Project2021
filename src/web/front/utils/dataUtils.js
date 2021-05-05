export function preprocessPatternsData(data) {
  const res = data.map((object) => {
    let date = new Date(object["date"]);
    date = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    return { ...object, date: date };
  });
  return res;
}
