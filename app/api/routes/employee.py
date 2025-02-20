from typing import Optional, Annotated, List
from uuid import UUID
import logging
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import (
    Path,
    Query,
    Security,
)

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repository.employee import EmployeeRepository
from app.repository.team import TeamRepository
from app.repository.vacation import VacationRepository
from app.schema.employee import EmployeeBase

router = APIRouter()


@router.get("/{employee_id}", response_model=Optional[EmployeeBase])
def get_employee(session: Annotated[Session, Depends(get_db)], *, employee_id: UUID):
    employee = EmployeeRepository.get(session=session, id=employee_id)
    # get team name
    team = TeamRepository.get(session=session, id=employee.team_id)
    return EmployeeBase(
        first_name=employee.first_name,
        last_name=employee.last_name,
        team_name=team.team_name,
    )


@router.get("/on_vacation", response_model=List[EmployeeBase])
def get_employees_on_vacation(
    session: Annotated[Session, Depends(get_db)],
    from_: Annotated[
        date,
        Query(alias="from", description="Start date for the range"),
    ],
    until: Annotated[
        Optional[date],
        Query(description="End date for the range"),
    ] = None,
    team_name: Annotated[Optional[str], Query(description="Team name")] = None,
):
    # if no value is provided for until, then consider a unique day, and set it to value of from_
    if not until:
        until = from_
    logging.debug(f"Getting employees on vacation from {from_} to {until} ...")

    # Find all vacations containing the search range
    vacations = VacationRepository.get_from_date_range(
        session=session, range_start_date=from_, range_end_date=until
    )
    # Then all employees
    employee_ids = [vacation.employee_id for vacation in vacations]
    employees = EmployeeRepository.get_by_ids(  # type: ignore
        session=session, employee_ids=employee_ids
    )
    logging.debug(
        f"Found {len(employees)} employees on vacation for this date range ..."
    )

    # If a team_name is provided, get the team_id from the database
    if team_name:
        team = TeamRepository.get_by_name(session=session, team_name=team_name)
        if not team:
            raise HTTPException(status_code=404, detail=f"Team {team_name!r} not found")
        team_id = team.id
        logging.debug(f"Found {team_name!r} in database, with {team_id=!r} ...")

        # then get the employees from the team
        team_employees = EmployeeRepository.get_by_team(  # type: ignore
            session=session, team_id=team_id
        )

        # filter the employees on vacation to keep only the ones from the team
        # Using the intersection of sets is more efficient
        employees = [
            e
            for e in employees
            if e.id in set(employee_ids) & {employee.id for employee in team_employees}
        ]
        logging.debug(
            f"Reducing employees list to {len(employees)}, keeping only those in team {team_name!r} ..."
        )

    return employees


@router.post("/", response_model=EmployeeBase)
def create_employee(session: Annotated[Session, Depends(get_db)], body: EmployeeBase):
    employee_name = f"{body.first_name} {body.last_name}"
    logging.debug(
        f"Trying to create new employee {employee_name!r} for team {body.team_name!r} ..."
    )

    # Check if the employee already exists
    employee = EmployeeRepository.get_by_name(  # type: ignore
        session=session,
        first_name=body.first_name,
        last_name=body.last_name,
    )
    if employee:
        raise HTTPException(
            status_code=400, detail=f"Employee {employee_name!r} already exists"
        )
    logging.debug(
        f"Ok, let us continue, Employee {employee_name!r} does not exist yet ..."
    )

    # Get the team_id from the database
    team = TeamRepository.get_by_name(session=session, team_name=body.team_name)
    if not team:
        raise HTTPException(
            status_code=404, detail=f"Team {body.team_name!r} not found"
        )
    team_id = team.id
    logging.info(f"{body.team_name!r} found in database, with {team_id=!r} ...")

    # Create the new instance in the database
    employee_data = {
        "first_name": body.first_name,
        "last_name": body.last_name,
        "team_id": team_id,
    }
    logging.debug(f"Creating new employee {employee_data=}")
    employee = EmployeeRepository.create(session=session, obj_in=employee_data)
    if not employee:
        raise HTTPException(status_code=400, detail="Employee could not be created")
    logging.info(f"{employee=} has been successfully created ...")

    return EmployeeBase(
        first_name=employee.first_name,
        last_name=employee.last_name,
        team_name=body.team_name,
    )
