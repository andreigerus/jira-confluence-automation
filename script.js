const ageForm = document.getElementById('ageForm');
const birthDateInput = document.getElementById('birthDate');
const targetDateInput = document.getElementById('targetDate');
const result = document.getElementById('result');
const numerologyPrediction = document.getElementById('numerologyPrediction');

const today = new Date();
const todayString = today.toISOString().split('T')[0];
birthDateInput.max = todayString;
targetDateInput.min = todayString;

const getLifePathNumber = date => {
  const digits = date.toISOString().split('T')[0].replace(/-/g, '');
  const reduce = value => {
    let total = value.toString().split('').reduce((sum, digit) => sum + Number(digit), 0);
    return total > 9 ? reduce(total) : total;
  };
  return reduce(digits);
};

const getNumerologyPrediction = lifePathNumber => {
  switch (lifePathNumber) {
    case 1:
      return 'You are a natural leader with independence, ambition, and creative drive.';
    case 2:
      return 'You are sensitive, supportive, and diplomatic, often bringing harmony to relationships.';
    case 3:
      return 'You have a joyful, expressive personality and thrive through communication and creativity.';
    case 4:
      return 'You are practical, dependable, and hardworking with a strong sense of order.';
    case 5:
      return 'You are adventurous, flexible, and thrive on freedom and new experiences.';
    case 6:
      return 'You are caring, responsible, and value family, community, and balance.';
    case 7:
      return 'You are thoughtful, introspective, and often drawn to learning, analysis, and solitude.';
    case 8:
      return 'You are ambitious, focused, and naturally inclined toward success, power, and achievement.';
    case 9:
      return 'You are compassionate, generous, and inspired to help others with a global perspective.';
    default:
      return 'Your personality is unique and shaped by a blend of intuition, creativity, and resilience.';
  }
};

ageForm.addEventListener('submit', event => {
  event.preventDefault();
  const birthDate = new Date(birthDateInput.value);
  const targetDate = targetDateInput.value ? new Date(targetDateInput.value) : null;

  if (!(birthDate instanceof Date) || isNaN(birthDate)) {
    result.textContent = 'Please enter a valid birth date.';
    numerologyPrediction.textContent = '';
    return;
  }

  if (birthDate > today) {
    result.textContent = 'Birth date cannot be in the future.';
    numerologyPrediction.textContent = '';
    return;
  }

  const lifePathNumber = getLifePathNumber(birthDate);
  numerologyPrediction.textContent = `Numerology personality prediction (${lifePathNumber}): ${getNumerologyPrediction(lifePathNumber)}`;

  const calculateAge = (fromDate, toDate) => {
    let years = toDate.getFullYear() - fromDate.getFullYear();
    let months = toDate.getMonth() - fromDate.getMonth();
    let days = toDate.getDate() - fromDate.getDate();

    if (days < 0) {
      months -= 1;
      const previousMonth = new Date(toDate.getFullYear(), toDate.getMonth(), 0);
      days += previousMonth.getDate();
    }

    if (months < 0) {
      years -= 1;
      months += 12;
    }

    return { years, months, days };
  };

  const currentAge = calculateAge(birthDate, today);
  let output = `You are ${currentAge.years} year${currentAge.years !== 1 ? 's' : ''}` +
    `, ${currentAge.months} month${currentAge.months !== 1 ? 's' : ''}` +
    `, and ${currentAge.days} day${currentAge.days !== 1 ? 's' : ''} old today.`;

  if (targetDate) {
    if (targetDate < birthDate) {
      result.textContent = 'Target date must be the same as or after your birth date.';
      return;
    }

    const futureAge = calculateAge(birthDate, targetDate);
    output += `\nIf you check on ${targetDate.toISOString().split('T')[0]}, you will be ${futureAge.years} year${futureAge.years !== 1 ? 's' : ''}` +
      `, ${futureAge.months} month${futureAge.months !== 1 ? 's' : ''}` +
      `, and ${futureAge.days} day${futureAge.days !== 1 ? 's' : ''} old.`;
  }

  result.innerText = output;
});
