from typing import Optional, Annotated
from uuid import UUID
from datetime import datetime
import logging

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repository.employee import EmployeeRepository
from app.repository.vacation import VacationRepository

from app.schema.vacation import VacationBase, VacationEmployeeBase


router = APIRouter()


@router.get("/{vacation_id}", response_model=Optional[VacationBase])
def get_vacation(session: Annotated[Session, Depends(get_db)], *, vacation_id: UUID):
    return VacationRepository.get(session=session, id=vacation_id)


@router.post("/", response_model=VacationBase, status_code=status.HTTP_201_CREATED)
def create_vacation(
    session: Annotated[Session, Depends(get_db)], body: VacationEmployeeBase
):
    logging.debug(f"Creating new vacation {body=}")

    if body.employee_name:
        first_name = body.employee_name.first_name
        last_name = body.employee_name.last_name
        employee_name = f"{first_name} {last_name}"
        logging.debug(f"{employee_name=}")
    else:
        raise HTTPException(status_code=400, detail="Employee name is required")

    # Check if the employee exists
    employee = EmployeeRepository.get_by_name(  # type: ignore
        session=session,
        first_name=first_name,
        last_name=last_name,
    )
    if not employee:
        raise HTTPException(
            status_code=404, detail=f"Employee {employee_name!r} not found"
        )
    else:
        logging.debug(f"Employee {employee_name!r} found")

    # Find all already existing vacations for this employee, ordered by start_date
    employee_vacations = VacationRepository.get_by_employee_id(
        session=session, employee_id=employee.id, order_by="start_date"
    )
    logging.debug(f"{employee_vacations=}")
    if employee_vacations:
        logging.debug(f"Found {len(employee_vacations)} vacations for {employee_name=}")
    else:
        logging.debug(f"No vacations found for {employee_name=}")

    # Find the first overlap between existing vacations and the new proposed one,
    # then modify the existing vacation accordingly
    overlap_found = False
    # TODO : debug below code, it seems to be wrong
    if body.start_date and body.end_date:
        for vacation in employee_vacations:
            if body.start_date <= vacation.start_date <= body.end_date:
                overlap_found = True
                VacationRepository.update(
                    session=session,
                    id=vacation.id,
                    data={"start_date": body.start_date},
                )
            if body.start_date <= vacation.end_date <= body.end_date:
                overlap_found = True
                VacationRepository.update(
                    session=session,
                    id=vacation.id,
                    data={"end_date": body.end_date},
                )
                logging.debug(f"Vacation {vacation.id!r} has been updated")
            if overlap_found:
                break

    # TODO : refine the logic, the case of a new vacation containing in full one or many existing ones
    #        is not taken into account yet

    # Create the vacation
    if not overlap_found:
        # TODO : improve this
        vacation_data = {
            "type": body.type.value,
            "start_date": body.start_date,
            "end_date": body.end_date,
            "employee_id": employee.id,
        }
        logging.debug(f"Creating new vacation with data {vacation_data=}")
        vacation = VacationRepository.create(
            session=session,
            obj_in=vacation_data,
        )
        if not vacation:
            raise HTTPException(status_code=400, detail="Vacation could not be created")
        logging.debug(
            f"Successfully created Vacation {vacation.id!r} for Employee {employee_name!r}"
        )
        logging.debug(f"{vacation=}")

    return VacationBase(**vacation.__dict__)


@router.put("/{vacation_id}", response_model=VacationBase)
def update_vacation(
    session: Annotated[Session, Depends(get_db)],
    *,
    vacation_id: UUID,
    body: VacationBase,
):
    vacation = VacationRepository.get(session=session, id=vacation_id)
    if not vacation:
        raise HTTPException(status_code=404, detail="Vacation not found")
    updated_vacation = VacationRepository.update(
        session=session, id=vacation_id, data=body.__dict__
    )
    logging.debug(f"Vacation with id {vacation_id} has been successfully updated")
    return VacationBase(**updated_vacation.__dict__)


@router.delete("/{vacation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vacation(session: Annotated[Session, Depends(get_db)], *, vacation_id: UUID):
    vacation = VacationRepository.get(session=session, id=vacation_id)
    if not vacation:
        raise HTTPException(status_code=404, detail="Vacation not found")
    VacationRepository.delete(session=session, id=vacation_id)
    logging.debug(f"Vacation with id {vacation_id} has been successfully deleted")
    return
