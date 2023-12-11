import React, {useEffect, useState} from 'react';
import axios from 'axios';
import {Table, Button, Container, Row, Col, InputGroup, ListGroup, Form} from 'react-bootstrap';

import 'bootstrap/dist/css/bootstrap.min.css';
import './Schedule.css';

const weekDay = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота"]
const defaultGroup = {
    "group": "6412-100503D",
    "link": "/rasp?groupId=531873998"
}

const Schedule = () => {
    const [data, setData] = useState();
    const [week, setWeek] = useState();
    const [elem, setElem] = useState(defaultGroup);
    const [search, setSearch] = useState("");
    const [match, setMatch] = useState([]);
  
    useEffect(()=> {
        axios("http://localhost:5000/currweek").then(response => {
            console.log(response.data.week);
            setWeek(response.data.week);
        });
    }, [])
    
    useEffect(()=> {
        if (week){
            axios('http://localhost:5000/schedule', {params: {group_link: elem.link, selectedWeek: week}}).then(response => {
            console.log(response.data);
            setData(response.data);
         });
        }
            
    }, [week, elem])

    const handleChange = (e) => {
        setSearch(e.target.value);
        console.log(e.target.value);

        axios.post("http://localhost:5000/entrys", {elem: e.target.value}).then(res => {
            const data = res.data;
            console.log(data);
            setMatch(data)

            console.log(match)

        })
        
      };

    function handleClick(elem) {
        console.log(elem)
        setSearch(elem);
        setMatch([]);
        setElem(elem);
    };

    function returnKey(elem) {
        
        if (Object.keys(elem).includes("name")) {
            return "name";
        }
        else {
            return "group";
        }
    }

    function nextWeek() {
        let tmp = parseInt(week);
        if (tmp + 1 < 50){
            tmp = tmp + 1;
        }
        setWeek(tmp);
    }

    function prevWeek() {
        let tmp = parseInt(week);
        if (tmp-1 > 0) {
            tmp = tmp - 1;
        }
        setWeek(tmp);
    }
    
    if (!data) return( <>...</>);

    return(
        <Container>
            <h2 className='container-header'>Расписание занятий для {elem[returnKey(elem)]}</h2>

            <InputGroup className="mb-3">
                <Form.Control
                    placeholder="Группа или преподаватель"
                    type="text"
                    value={search? search[returnKey(search)] : ""}
                    onChange={handleChange}
                    aria-describedby="basic-addon2"
                />  
            </InputGroup>

            <Container className='scroll border'>
                {match.length > 0 && (
                    <ListGroup>  
                    {match.map((elem) => (
                        <ListGroup.Item className="d-flex justify-content-center align-items-center" 
                                        action
                                        onClick={() => handleClick(elem)} 
                                        key={elem[returnKey(elem)]}>
                            {elem[returnKey(elem)]}
                        </ListGroup.Item>
                    ))}
                    </ListGroup>
                )}   
            </Container>
            

            <Container className='border border-primary container'>
                <Row>
                    <Button variant="primary" className="button-style small-table" onClick={prevWeek}>
                    Предыдущая неделя
                    </Button>
                    <Col>
                        <div className="d-flex justify-content-center">
                            <h5>Неделя {week}</h5>
                        </div>
                    </Col >
                        
                    <Button variant="primary" className="float-end button-style small-table" onClick={nextWeek}>
                    Следующая неделя
                    </Button>
                </Row>
                
                <Table bsPrefix="table table-bordered border border-primary small-table" borderless size="sm">
                    <thead>
                        <tr>
                        <th style={{ width: '5%' }}>Время</th>
                        {weekDay.map((day, index) => (
                            <th key={index} style={{ width: '11%' }}>{day}</th>
                        ))}
                        
                        </tr>
                    </thead>
                    <tbody>
                        {Array.from({ length: data["понедельник"].length}).map((_, index) => (
                            <tr key={index}>
                                <td>
                                    {data["понедельник"][index]["time"]}
                                </td>
                                {weekDay.map((day, index_inner) => (
                                    <td key={index_inner}>
                                        {data[day][index]["discipline"] + '\n'}<br/>
                                        {data[day][index]["place"] + '\n'}<br/>
                                        {data[day][index]["teacher"] + '\n'}<br/>
                                        {data[day][index]["groups"]}
                                    </td>
                                ))}
                            </tr>
                        ))}

                    </tbody>
                </Table>
            </Container>     
        </Container>     
    );
  }
    
  export default Schedule;