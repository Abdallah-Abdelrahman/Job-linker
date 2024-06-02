/**
 * utility to format date from current time
 * @param {Date} date - date object
 * @returns string format in `today`, `yesterday`, `last week`, `Month year`
 */
function formatFromNow(date: Date) {
  const now = new Date();
  const dateToFormat = new Date(date);

  // Calculate the difference in days
  const diffTime = Math.abs(now - dateToFormat);
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

  // Check if the date is today, yesterday, or within the last week
  if (diffDays === 0) {
    return 'today';
  } else if (diffDays === 1) {
    return 'yesterday';
  } else if (diffDays <= 7) {
    return 'last week';
  } else {
    // Format the date to display month and year if more than a week ago
    return new Intl.DateTimeFormat('en-US', { month: 'long', year: 'numeric' }).format(dateToFormat);
  }
}

/**
 * utility to format date
 * @param {Date} date - date object
 * @returns string format in `Month year`
 */
function formateDate(date: Date) {
  return new Date(date).toLocaleDateString('en', { year: 'numeric', month: 'short' });
}
export { formatFromNow, formateDate };
