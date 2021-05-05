export function preprocessPatternsData(data) {
  const res = data.map((object) => {
    return { ...object, date: new Date(object["date"]) };
  });
  return res;
}
