export function preprocessPatternsData(data) {
  return data.map((object) => {
    return { ...object, date: Date(object["date"]) };
  });
}
