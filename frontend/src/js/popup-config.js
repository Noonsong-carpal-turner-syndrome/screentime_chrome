export const GRAPH_SIZE = 250;
export function isEmpty(obj) {
  return obj && Object.keys(obj).length === 0;
}
export const getColorOfCategory = (name) => {
  let color;
  switch (name) {
    case "ent":
      color = "#ffa600";
      break;
    case "prod":
      color = "#ff7c43";
      break;
    case "sns":
      color = "#f95d6a";
      break;
    case "shop":
      color = "#a05195";
      break;
    case "edu":
      color = "#665191";
      break;
    case "car":
      color = "#2f4b7c";
      break;
    case "etc":
      color = "#003f5c";
      break;
    default:
      color = "#969696";
      break;
  }
  return color;
};

export const getDateString = (before) => {
  let date = new Date();
  if (before !== undefined) {
    date.setDate(date.getDate() - before);
  }
  let year = date.getFullYear();
  let month = date.getMonth() + 1;
  let d = date.getDate();
  let dateString;

  month = month < 10 ? "0" + month : month;
  d = d < 10 ? "0" + d : d;
  dateString = `${year}-${month}-${d}`;

  return dateString;
};

export function getTimeString(second) {
  let tempSec = second;
  let hour = Math.floor(tempSec / (60 * 60));
  tempSec = tempSec - hour * 60 * 60;
  let min = Math.floor(tempSec / 60);
  tempSec = tempSec - min * 60;
  let sec = tempSec;
  let hourString = "";
  let minString = "";
  let secString = "";
  if (hour) {
    hour = hour < 10 ? "0" + hour : hour;
    hourString = `${hour}시간 `;
  }
  min = min < 10 ? "0" + min : min;
  sec = sec < 10 ? "0" + sec : sec;
  minString = `${min}분`;
  secString = `${sec}초`;
  return `${hourString}${minString}${secString}`;
}
export const CATEGORIES = {
  ent: {
    name: "엔터테인먼트",
  },
  prod: {
    name: "생산성 및 금융",
  },
  sns: {
    name: "소셜미디어",
  },
  shop: {
    name: "쇼핑 및 음식",
  },
  edu: {
    name: "학습",
  },
  car: {
    name: "사무 및 경력",
  },
  etc: {
    name: "기타",
  },
  auto: {
    name: "자동",
  },
};

const MIN_PERCENTAGE_GRAPH = 7;
