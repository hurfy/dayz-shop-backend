from sqlalchemy   import select

from shop.schemas import SProductGet, SProductCreate, SProductUpdate, SProductPartialUpdate
from shop.models  import MProduct
from database     import new_session


class ProductRepository:
    @classmethod
    async def fetch_product_list(cls) -> list[SProductGet]:
        """Get list of products ..."""
        async with new_session() as session:
            # Execute SQL query to fetch all data from MProduct
            result = await session.execute(
                select(MProduct)
            )

            # Extract all MProduct objects from query result
            product_models = result.scalars().all()

            # Serialize MProduct objects to SProductGet using validation
            return [
                SProductGet.model_validate(product_model)
                for product_model in product_models
            ]

    @classmethod
    async def fetch_product(cls, product_id: int) -> SProductGet:
        """Get product by ID ..."""
        async with new_session() as session:
            # Fetch all data from MProduct where id == product_id
            result = await session.execute(
                select(MProduct).where(MProduct.id == product_id)
            )

            # HTTP 404
            if not (product := result.scalars().first()):
                raise ValueError(f"Product with ID {product_id} not found.")

            # Extract MProduct object from query result
            return SProductGet.model_validate(product)

    @classmethod
    async def create_product(cls, product_data: SProductCreate) -> SProductGet:
        """Create a product ..."""
        async with new_session() as session:
            # Product data as dict
            data = product_data.model_dump()

            # Fix me
            if "image_url" in data:
                data["image_url"] = str(data["image_url"])

            # Add to session
            product = MProduct(**data)
            session.add(product)

            # Applying the changes
            await session.flush()
            await session.commit()

            return SProductGet.model_validate(product)


    @classmethod
    async def update_product(
            cls, product_id: int, product_data: SProductUpdate | SProductPartialUpdate, partial: bool
    ) -> SProductGet:
        """Update | Partial update the product ..."""
        async with new_session() as session:
            # Fetch all data from MProduct where id == product_id
            result = await session.execute(
                select(MProduct).where(MProduct.id == product_id)
            )

            # HTTP 404
            if not (product := result.scalars().first()):
                raise ValueError(f"Product with ID {product_id} not found")

            # Product data as dict
            data = product_data.model_dump(exclude_unset=partial)

            # Fix me
            if "image_url" in data:
                data["image_url"] = str(data["image_url"])

            # Modifying the data
            for key, value in data.items():
                setattr(product, key, value)

            # Applying the changes
            await session.commit()

            return SProductGet.model_validate(product)

    @classmethod
    async def delete_product(cls, product_id: int) -> None:
        """Delete the product ..."""
        async with new_session() as session:
            # Fetch all data from MProduct where id == product_id
            result = await session.execute(
                select(MProduct).where(MProduct.id == product_id)
            )

            # HTTP 404
            if not (product := result.scalars().first()):
                raise ValueError(f"Product with ID {product_id} not found")

            # Applying the changes
            await session.delete(product)
            await session.commit()