// src/App.js
import React, { useState, useEffect } from 'react';
import './App.css';

const API_URL = 'http://127.0.0.1:8000/events';

function App() {
  const [events, setEvents] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    start_date: '',
    start_time: '',
    duration_minutes: '',
    recurring_days_of_week: []
  });

  // Define day names to map indices to names.
  const dayNames = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
  ];

  const fetchEvents = async () => {
    try {
      const response = await fetch(API_URL);
      const data = await response.json();
      setEvents(data);
    } catch (error) {
      console.error('Error fetching events:', error);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, []);

  const handleSubmit = async e => {
    e.preventDefault();
    const payload = {
      ...formData,
      duration_minutes: parseInt(formData.duration_minutes),
      recurring_days_of_week: formData.recurring_days_of_week.length
        ? formData.recurring_days_of_week.map(Number)
        : null
    };
    try {
      await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      setFormData({
        name: '',
        start_date: '',
        start_time: '',
        duration_minutes: '',
        recurring_days_of_week: []
      });
      fetchEvents();
    } catch (error) {
      console.error('Error creating event:', error);
    }
  };

  const handleDelete = async id => {
    try {
      await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
      fetchEvents();
    } catch (error) {
      console.error('Error deleting event:', error);
    }
  };

  const handleChange = e => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleCheckboxChange = e => {
    const { value, checked } = e.target;
    setFormData(prev => {
      let newArray = prev.recurring_days_of_week;
      if (checked) {
        newArray = [...newArray, value];
      } else {
        newArray = newArray.filter(v => v !== value);
      }
      return { ...prev, recurring_days_of_week: newArray };
    });
  };

  return (
    <div className='App'>
      <h1>SchedulePro Dashboard</h1>
      <section>
        <h2>Create New Event</h2>
        <form onSubmit={handleSubmit}>
          <div>
            <label>Event Name: </label>
            <input
              type='text'
              name='name'
              value={formData.name}
              onChange={handleChange}
              required
            />
          </div>
          <div>
            <label>Start Date: </label>
            <input
              type='date'
              name='start_date'
              value={formData.start_date}
              onChange={handleChange}
              required
            />
          </div>
          <div>
            <label>Start Time: </label>
            <input
              type='time'
              name='start_time'
              value={formData.start_time}
              onChange={handleChange}
              required
            />
          </div>
          <div>
            <label>Duration (minutes): </label>
            <input
              type='number'
              name='duration_minutes'
              value={formData.duration_minutes}
              onChange={handleChange}
              required
            />
          </div>
          <div>
            <label>Recurring Days: </label>
            <div>
              {dayNames.map((day, index) => (
                <label key={index}>
                  <input
                    type='checkbox'
                    value={index}
                    onChange={handleCheckboxChange}
                  />{' '}
                  {day}
                </label>
              ))}
            </div>
          </div>
          <button type='submit'>Submit</button>
        </form>
      </section>
      <hr />
      <section>
        <h2>Scheduled Events</h2>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Date / Recurrence</th>
              <th>Time</th>
              <th>Duration</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {events.map(event => (
              <tr key={event.id}>
                <td>{event.id}</td>
                <td>{event.name}</td>
                <td>
                  {event.recurring_days_of_week
                    ? 'Recurring: ' +
                      event.recurring_days_of_week
                        .map(num => dayNames[num])
                        .join(', ')
                    : event.start_date}
                </td>
                <td>{event.start_time}</td>
                <td>{event.duration_minutes} mins</td>
                <td>
                  <button onClick={() => handleDelete(event.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}

export default App;
